from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from ..conf import settings
from .. import decorators
from .. import mixins


class ProjectsViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/projects.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    def get(self, request):

        if len(settings.ALLOWED_PROJECT_IDS) == 1:
            return redirect(
                reverse(
                    settings.URLNAME_ITEMS,
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

        return {
            'page': {
                'title': _('Projects'),
                'sub_title': ''
            },
            'results': [],
        }
