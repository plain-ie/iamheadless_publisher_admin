from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from ..conf import settings
from .. import decorators
from .. import mixins
from .. import utils


class ItemViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/item.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def get(self, request, project_id, item_type, item_id, tenant_id=None):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def post(self, request, project_id, item_type, item_id, tenant_id=None):

        context = self.get_context()

        serializer = self.get_item_type_serializer(item_type)

        try:
            validated_data = serializer.validate_form(request, context['data'])

        except ValidationError as e:
            print(str(e))
            messages.error(request, _('Item updated failed'))

        else:

            user = self.get_request_user()

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
                _('Item updated successfully')
            )

            serializer.post_update(request, validated_data)

            redirect_url_kwargs = {
                'project_id': project_id,
                'item_type': item_type,
                'item_id': item_id,
            }

            if tenant_id is not None:
                redirect_url_kwargs['tenant_id'] = tenant_id

            redirect_url = reverse(
                settings.URLNAME_ITEM,
                kwargs=redirect_url_kwargs
            )

            return redirect(redirect_url)

        return render(
            request,
            self.template,
            context=context
        )

    def get_context(self):

        item_type = self.get_item_type()
        serializer = self.get_item_type_serializer(item_type)

        if serializer is None:
            raise ValueError(f'Serializer for "{item_type}" not found')  # XXXX TODO: Translate

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
            }
        }

    def get_delete_url(self):

        item_id = self.get_item_id()
        item_type = self.get_item_type()
        project_id = self.get_project_id()
        tenant_id = self.get_tenant_id()

        kwargs = {
            'project_id': project_id,
            'item_type': item_type,
            'item_id': item_id,
        }

        if tenant_id is not None:
            kwargs['tenant_id'] = tenant_id

        return reverse(settings.URLNAME_ITEM_DELETE, kwargs=kwargs)

    def get_preview_url(self):
        return '#'

    def get_create_url(self):

        item_type = self.get_item_type()
        project_id = self.get_project_id()
        tenant_id = self.get_tenant_id()

        kwargs = {
            'project_id': project_id,
            'item_type': item_type,
        }

        if tenant_id is not None:
            kwargs['tenant_id'] = tenant_id

        return reverse(settings.URLNAME_ITEM_CREATE_STEP_THREE, kwargs=kwargs)


class ItemCreationWorkFlowStepOne(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/item_creation.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def get(self, request, project_id):

        formated_choices = []

        project_id = self.get_project_id()
        user = self.get_request_user()

        choices = utils.get_user_item_types_choices(project_id, user)

        for choice in choices:

            url = reverse(
                settings.URLNAME_ITEM_CREATE_STEP_TWO,
                kwargs={
                    'project_id': project_id,
                    'item_type': choice[0]
                }
            )

            formated_choices.append({
                'url': url,
                'title': choice[1],
            })

        context = {
            'choices': formated_choices,
            'page': {
                'title': _('item creation'),
                'sub_title': _('select item type'),
            },
            'request_kwargs': {
                'project_id': self.get_project_id(),
                'tenant_id': self.get_tenant_id(),
            },
        }

        return render(
            request,
            self.template,
            context=context
        )


class ItemCreationWorkFlowStepTwo(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/item_creation.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def get(self, request, project_id, item_type):

        formated_choices = []

        project_id = self.get_project_id()
        item_type = self.get_item_type()
        user = self.get_request_user()

        serializer = self.get_item_type_serializer(item_type)
        if serializer._tenant_required is False:
            url = reverse(
                settings.URLNAME_ITEM_CREATE_STEP_THREE,
                kwargs={
                    'project_id': project_id,
                    'item_type': item_type
                }
            )
            return redirect(url)

        choices = utils.get_user_tenants_choices(project_id, user)

        for choice in choices:

            url = reverse(
                settings.URLNAME_ITEM_CREATE_STEP_THREE,
                kwargs={
                    'project_id': project_id,
                    'tenant_id': choice[0],
                    'item_type': item_type
                }
            )

            formated_choices.append({
                'url': url,
                'title': choice[1],
            })

        context = {
            'choices': formated_choices,
            'page': {
                'title': _('item creation'),
                'sub_title': _('select tenant'),
            },
            'request_kwargs': {
                'project_id': self.get_project_id(),
            },
        }

        return render(
            request,
            self.template,
            context=context
        )


class ItemCreationWorkFlowStepThree(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/item.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def get(self, request, project_id, item_type, tenant_id=None):

        context = self.get_context()

        return render(
            request,
            self.template,
            context=context
        )

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def post(self, request, project_id, item_type, tenant_id=None):

        user = self.get_request_user()
        serializer = self.get_item_type_serializer(item_type)
        context = self.get_context()

        try:
            validated_data = serializer.validate_form(self.request, {})

        except ValidationError:
            messages.error(request, _('Item creation failed'))

        else:

            validated_data = serializer.pre_create(request, validated_data)

            req = self.get_client().create_item(
                project_id=project_id,
                tenant_id=tenant_id,
                item_type=item_type,
                data=validated_data,
                token=self.get_request_user_token()
            )

            messages.success(
                request,
                _('Item created successfully')
            )

            serializer.post_create(request, validated_data)

            redirect_url_kwargs = {
                'project_id': project_id,
                'item_type': item_type,
                'item_id':  req['id']
            }

            if tenant_id is not None:
                redirect_url_kwargs['tenant_id'] = tenant_id

            return redirect(
                reverse(
                    settings.URLNAME_ITEM,
                    kwargs=redirect_url_kwargs
                )
            )

        return render(
            request,
            self.template,
            context=context
        )

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
                'title': _('item creation'),
                'sub_title': serializer._display_name_plural
            },
            'request_kwargs': {
                'project_id': project_id,
                'tenant_id': tenant_id,
                'item_type': self.get_item_type(),
                'item_id': self.get_item_id(),
            },
            'tenant': tenant,
        }


class ItemDeleteViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.tenant_has_project_access(), name='dispatch')
    @method_decorator(decorators.user_has_tenant_access(), name='dispatch')
    @method_decorator(decorators.user_has_item_type_access(), name='dispatch')
    def get(self, request, project_id, item_type, item_id, tenant_id=None):

        client = self.get_client()
        serializer = self.get_item_type_serializer(item_type)

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

        return redirect(
            reverse(
                settings.URLNAME_ITEMS,
                kwargs={
                    'project_id': project_id
                }
            )
        )
