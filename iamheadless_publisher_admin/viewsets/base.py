from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import View

from ..conf import settings
from .. import decorators
from .. import mixins
from .. import utils


class BaseItemCreateViewSet(
        mixins.ItemViewSetPermissionMixin,
        mixins.UtilsViewSetMixin,
        View):

    template = 'iamheadless_publisher_admin/pages/item.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    def get(self, request, project_id, tenant_id=None):
        self.has_access()
        return render(request, self.template, context=self.get_context())

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    def post(self, request, project_id, tenant_id=None):

        self.has_access()

        user = self.get_request_user()
        serializer = self.get_item_type_serializer()
        context = self.get_context()

        try:
            validated_data = serializer.validate_form(self.request, {})

        except ValidationError:
            messages.error(request, 'Item creation failed')

        else:

            validated_data = serializer.pre_create(request, validated_data)

            req = self.get_client().create_item(
                project_id=project_id,
                tenant_id=tenant_id,
                item_type=self.item_type,
                data=validated_data,
                token=self.get_request_user_token()
            )

            messages.success(
                request,
                'Item created successfully'
            )

            serializer.post_create(request, validated_data)

            return redirect(self.get_retrieve_url(item_id=req['id']))

        return render(request, self.template, context=context)

    def get_context(self):

        tenant = None

        project_id = self.get_project_id()
        tenant_id = self.get_tenant_id()

        item_type = self.get_item_type()
        serializer = self.get_item_type_serializer(item_type)

        initial_data = {}

        if tenant_id is not None:

            tenant = self.get_client().project_tenant(
                tenant_id,
                project_id,
            )

            if tenant is None:
                raise ObjectDoesNotExist('Tenant does not exist')

        return {
            'data': initial_data,
            'form_html': serializer.render_form(self.request, initial_data),
            'page': {
                'title': 'item creation',
                'sub_title': serializer._display_name_plural
            },
            'request_kwargs': {
                'project_id': project_id,
                'tenant_id': tenant_id,
                'item_type': self.get_item_type(),
                'item_id': self.get_item_id(),
            },
            'tenant': tenant,
            'urls': {
                'step_two': '#',
                'step_one': '#',
            }
        }

    #

    def get_retrieve_url(self):
        return '#'

    #

    @classmethod
    def get_route(cls, prefix=''):
        return None

    @classmethod
    def get_urlpatterns(cls, prefix=''):
        route = cls.get_route(prefix=prefix)
        if route is not None:
            return [route, ]
        return []


class BaseItemRetrieveUpdateViewSet(
        mixins.ItemViewSetPermissionMixin,
        mixins.UtilsViewSetMixin,
        View):

    item_type = None
    pydantic_model = None
    template = None

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    def get(self, request, project_id, item_id, tenant_id=None):
        self.has_access()
        return render(request, self.template, context=self.get_context())

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    def post(self, request, project_id, item_id, tenant_id=None):

        self.has_access()

        context = self.get_context()
        serializer = self.get_item_type_serializer()

        try:
            validated_data = serializer.validate_form(request, context['data'])

        except ValidationError as e:
            print(str(e))
            messages.error(request, 'Item updated failed')

        else:
            validated_data = serializer.pre_update(request, validated_data)

            req = self.get_client().update_item(
                project_id=project_id,
                tenant_id=tenant_id,
                item_id=item_id,
                data=validated_data,
                token=self.get_request_user_token()
            )

            messages.success(
                request,
                'Item updated successfully'
            )

            serializer.post_update(request, validated_data)

            redirect_url_kwargs = {
                'project_id': project_id,
                'item_type': self.item_type,
                'item_id': item_id,
            }

            if tenant_id is not None:
                redirect_url_kwargs['tenant_id'] = tenant_id

            return redirect(self.get_retrieve_url())

        return render(request, self.template, context=context)

    def get_context(self):

        item_type = self.get_item_type()
        serializer = self.get_item_type_serializer()

        if serializer is None:
            raise ValueError(f'Serializer for "{item_type}" not found')

        tenant = None

        client = self.get_client()
        item_id = self.get_item_id()
        project_id = self.get_project_id()
        tenant_id = self.get_tenant_id()

        item = client.retrieve_item(
            project_id=project_id,
            tenant_id=tenant_id,
            item_id=item_id,
            token=self.get_request_user_token()
        )

        if item is None:
            raise ObjectDoesNotExist('Item does not exist')

        serialized_data = serializer(**item)

        data = serialized_data.DATA

        form_html = serializer.render_form(self.request, data)

        if tenant_id is not None:

            tenant = client.project_tenant(
                tenant_id,
                project_id,
            )

            if tenant is None:
                raise ObjectDoesNotExist('Tenant does not exist')

        return {
            'data': data,
            'form_html': form_html,
            'page': {
                'title': serialized_data.TITLE,
                'sub_title': None,
            },
            'request_kwargs': {
                'project_id': self.get_project_id(),
                'tenant_id': self.get_tenant_id(),
                'item_type': self.get_item_type(),
                'item_id': self.get_item_id(),
            },
            'serializer': serialized_data,
            'tenant': tenant,
            'urls': {
                'create': self.get_create_url(),
                'delete': self.get_delete_url(),
                'preview': self.get_preview_url(),
                'retrieve': self.get_retrieve_url(),
            }
        }

    # URL

    def get_delete_url(self):
        return '#'

    def get_preview_url(self):
        return '#'

    def get_create_url(self):
        return '#'

    def get_retrieve_url(self):
        return self.request.path

    #

    @classmethod
    def get_route(cls, prefix=''):
        return None

    @classmethod
    def get_urlpatterns(cls, prefix=''):
        route = cls.get_route(prefix=prefix)
        if route is not None:
            return [route, ]
        return []


class BaseItemDeleteViewSet(
        mixins.ItemViewSetPermissionMixin,
        mixins.UtilsViewSetMixin,
        View):

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    def get(self, request, project_id, item_id, tenant_id=None):

        self.has_access()

        client = self.get_client()
        serializer = self.get_item_type_serializer()

        item = client.retrieve_item(
            project_id=project_id,
            item_id=self.get_item_id(),
            token=self.get_request_user_token()
        )

        serializer.pre_delete(request, item)

        req = client.delete_item(
            project_id=project_id,
            item_id=item_id,
            token=self.get_request_user_token()
        )

        serializer.post_delete(request, item)

        return redirect(self.get_item_list_url())

    #

    def get_item_list_url(self):
        return reverse(
            settings.URLNAME_ITEMS,
            kwargs={
                'project_id': self.get_project_id()
            }
        )

    #

    @classmethod
    def get_route(cls, prefix=''):
        return None

    @classmethod
    def get_urlpatterns(cls, prefix=''):
        route = cls.get_route(prefix=prefix)
        if route is not None:
            return [route, ]
        return []
