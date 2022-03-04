from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from ..conf import settings
from .. import decorators
from .. import mixins


class DashboardViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/homepage.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def get(self, request, project_id=None):

        if project_id is None:
            return redirect(
                reverse(
                    settings.URLNAME_DASHBOARD,
                    kwargs={
                        'project_id': settings.ALLOWED_PROJECT_IDS[0]
                    }
                )
            )

        return render(
            request,
            self.template,
            context=self.get_context()
        )

    def get_context(self):

        req = self.get_client().retrieve_items(
            project_id=self.get_project_id(),
            count=5,
            token=self.get_request_user_token(),
        )

        results = req['results']
        total = req['total']

        req2 = self.get_client().retrieve_items(
            project_id=self.get_project_id(),
            count=1,
            published=True,
            token=self.get_request_user_token(),
        )

        total2 = req2['total']

        return {
            'page': {
                'title': _('Dashboard'),
                'sub_title': _('Publishing overview')
            },
            'results': results,
            'stats': [
                {
                    'title': _('Published items'),
                    'value': total2,
                },
                {
                    'title': _('Total items'),
                    'value': total,
                }
            ]
        }


class HomepageViewSet(View):

    def get(self, request, language=None):

        return redirect(
            reverse(
                settings.URLNAME_SIGN_IN
            )
        )
