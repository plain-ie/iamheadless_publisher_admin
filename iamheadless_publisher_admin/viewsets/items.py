import json

from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from ..conf import settings
from .. import decorators
from .. import mixins
from .. import utils


class ItemListViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    client = utils.get_client()

    template = 'iamheadless_publisher_admin/pages/items.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def get(self, request, project_id):

        context = self.get_context()

        format = request.GET.get('format', None)
        if format == 'json':
            return HttpResponse(
                json.dumps({
                    'page': context['pagination']['page'],
                    'pages': context['pagination']['pages'],
                    'total': context['pagination']['total'],
                    'results': list(map(lambda x: json.loads(x.json()), context['results'])),
                }),
                content_type='application/json'
            )

        return render(
            request,
            self.template,
            context=context
        )

    def get_context(self):

        params = getattr(self.request, self.request.method)
        project_id = self.get_project_id()

        tenant_ids = params.getlist('tenant', None)
        tenant_ids = list(filter(lambda x: x != '', tenant_ids))
        if len(tenant_ids) == 0:
            tenant_ids = None

        item_types = params.getlist('item_type', None)
        item_types = list(filter(lambda x: x != '', item_types))
        if len(item_types) == 0:
            item_types = None

        statuses = params.getlist('status', None)

        published = 'published' in statuses
        if published is False:
            published = None

        unpublished = 'unpublished' in statuses
        if unpublished is False:
            unpublished = None

        req = self.client.retrieve_items(
            project_id=project_id,
            tenant_id=tenant_ids,
            item_type=item_types,
            token=self.get_request_user_token(),
            published=published,
            unpublished=unpublished,
        )

        item_types_choices = self.get_item_types_choices()
        tenants_choices = self.get_tenants_choices()
        statuses = self.get_statuses_choices()

        return {
            'choices': {
                'item_types': item_types_choices,
                'tenants': tenants_choices,
                'statuses': statuses,
            },
            'form': None,
            'page': {
                'title': _('Publish items'),
            },
            'pagination': {
                'page': req['page'],
                'pages': req['pages'],
                'total': req['total'],
                'next_url': None,
                'previous_url': None,
            },
            'request_kwargs': {
                'project_id': project_id,
            },
            'results': req['results'],
        }

    def get_item_types_choices(self):
        user = self.get_request_user()
        project_id = self.get_project_id()
        return utils.get_user_item_types_choices(project_id, user)

    def get_tenants_choices(self):
        project_id = self.get_project_id()
        user = self.get_request_user()
        return utils.get_user_tenants_choices(project_id, user)

    def get_statuses_choices(self):
        return [
            ['published', _('published')],
            ['unpublished', _('unpublished')]
        ]
