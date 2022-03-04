from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from iamheadless_signer.lookups.sign import sign_object
from iamheadless_signer.lookups.unsign import unsign_object

from ..conf import settings
from .. import decorators
from .. import utils


class RequestPasswordResetLinkViewSet(View):

    client = utils.get_client()
    template = 'iamheadless_publisher_admin/pages/authentication/request_reset_link.html'

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def get(self, request):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def post(self, request):

        params = getattr(request, request.method)

        email = params.get('email')

        # XXXX TODO
        # CHECK IF USER WITH EMAIL EXISTS

        data = {
            'email': email
        }

        signed_data = sign_object(data, settings.SECRET_KEY, settings.RESET_LINK_MAX_AGE)

        reset_link = reverse(
            settings.URLNAME_RESET_PASSWORD,
            kwargs={
                'token': signed_data['data']
            }
        )

        self.client.send_reset_link(email, reset_link)

        messages.success(request, _('Reset link has been sent to email provided'))

        return redirect(settings.URLNAME_REQUEST_PASSWORD_RESET_LINK)

    def get_context(self):
        return {
            'page': {
                'title': settings.PROJECT_TITLE,
                'sub_title': 'Request password reset link',
            }
        }


class ResetPasswordViewSet(View):

    client = utils.get_client()
    template = 'iamheadless_publisher_admin/pages/authentication/reset_password.html'

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def get(self, request, token):

        context = self.get_context()
        unsigned_data = unsign_object(token, settings.SECRET_KEY, settings.RESET_LINK_MAX_AGE)

        if 'message' in unsigned_data:
            messages.error(request, _('Token has expired or was tampered with!'))
            context['token_is_invalid'] = True

        return render(
            request,
            self.template,
            context=context
        )

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def post(self, request, token):

        params = getattr(request, request.method)

        email = params.get('email')
        password = params.get('password')
        password2 = params.get('password2')

        error_url = reverse(
            settings.URLNAME_RESET_PASSWORD,
            kwargs={
                'token': token,
            }
        )

        if password != password2:
            messages.error(request, _('Passwords do not match'))
            return redirect(error_url)

        unsigned_data = unsign_object(token, settings.SECRET_KEY, settings.RESET_LINK_MAX_AGE)

        if 'message' in unsigned_data:
            messages.error(request, _('Token has expired or was tampered with!'))
            return redirect(error_url)

        try:
            signed_email = unsigned_data['data']['email']
        except KeyError:
            messages.error(request, _('Malformed token data'))
            return redirect(error_url)

        if email != signed_email:
            messages.error(request, _('Token is signed with different email'))
            return redirect(error_url)

        self.client.reset_password(signed_email, password)
        messages.success(request, _('Password reset successfull!'))

        return redirect(settings.URLNAME_SIGN_IN)

    def get_context(self):
        return {
            'page': {
                'title': settings.PROJECT_TITLE,
                'sub_title': _('reset password')
            }
        }


class SignInViewSet(View):

    template = 'iamheadless_publisher_admin/pages/authentication/sign_in.html'

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def get(self, request):
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(decorators.unauthenticated_user_required(), name='dispatch')
    def post(self, request):

        params = getattr(request, request.method)
        email = params.get('email')
        password = params.get('password')
        next = params.get('next', None)

        client = utils.get_client()
        req = client.sign_in(request, email, password)

        if req is not None:
            if next is not None and next != '':
                return redirect(next)
            return redirect(settings.URLNAME_PROJECTS)

        messages.error(request, _('Check your credentials, sign in failed.'))

        return redirect(settings.URLNAME_SIGN_IN)

    def get_context(self):
        return {
            'page': {
                'title': settings.PROJECT_TITLE,
                'sub_title': _('sign in')
            }
        }


class SignOutViewSet(View):

    @method_decorator(decorators.login_required(), name='dispatch')
    def get(self, request):
        client = utils.get_client()
        client.sign_out(request)
        return redirect(settings.URLNAME_SIGN_IN)
