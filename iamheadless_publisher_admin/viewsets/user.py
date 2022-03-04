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


class UserProfileViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/user/profile.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def get(self, request, project_id):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def post(self, request, project_id):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    def get_context(self):
        return {}


class UserProjectProfileViewSet(
        mixins.UtilsViewSetMixin,
        View
        ):

    template = 'iamheadless_publisher_admin/pages/user/project_profile.html'

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def get(self, request, project_id, item_type, item_id, tenant_id=None):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(decorators.login_required(), name='dispatch')
    @method_decorator(decorators.user_has_project_access(), name='dispatch')
    def post(self, request, project_id):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    def get_context(self):
        return {}
