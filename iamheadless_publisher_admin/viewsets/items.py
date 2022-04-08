import json
import re

from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
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
    count = settings.ITEMS_LIST_LENGTH
    page_param_name = 'page'

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
        item_types_choices = self.get_item_types_choices()

        tenant_ids = params.getlist('tenant', None)
        tenant_ids = list(filter(lambda x: x != '', tenant_ids))
        if len(tenant_ids) == 0:
            tenant_ids = None

        allowed_item_types = list(map(lambda x: x[0], item_types_choices))
        requested_item_types = params.getlist('item_type', None)
        requested_item_types = list(filter(lambda x: x != '', requested_item_types))

        if len(requested_item_types) != 0:
            item_types = list(set(allowed_item_types).intersection(requested_item_types))
        else:
            item_types = None

        page = self.get_page()

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
            page=int(page),
            count=self.count,
        )

        tenants_choices = self.get_tenants_choices()
        statuses = self.get_statuses_choices()

        page = req['page']
        pages = req['pages']

        return {
            'choices': {
                'item_types': item_types_choices,
                'tenants': tenants_choices,
                'statuses': statuses,
            },
            'form': None,
            'page': {
                'title': 'Publish items',
            },
            'pagination': {
                'page': page,
                'pages': pages,
                'total': req['total'],
                'next_url': self.get_next_url(pages),
                'previous_url': self.get_previous_url(),
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
            ['published', 'published'],
            ['unpublished', 'unpublished']
        ]

    def get_page(self):
        params = getattr(self.request, self.request.method)
        page = params.get(self.page_param_name, '1')
        if page.isdigit() is False:
            page = '1'
        return int(page)

    def change_page_in_url(self, page):

        prefix = '?'
        url = self.request.build_absolute_uri()

        if prefix in url:
            prefix = '&'

        if f'{self.page_param_name}=' not in url:
            url = url + prefix + f'{self.page_param_name}=1'

        url = re.sub(
            rf'{self.page_param_name}\=[0-9]*',
            f'{self.page_param_name}={page}',
            url
        )

        return url

    def get_next_url(self, pages):
        page = self.get_page()
        if page < pages:
            next_page = page + 1
            return self.change_page_in_url(next_page)
        return None

    def get_previous_url(self):
        page = self.get_page()
        if page > 1:
            previous_page = page - 1
            return self.change_page_in_url(previous_page)
        return None
