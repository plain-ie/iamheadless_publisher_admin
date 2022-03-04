from django.shortcuts import reverse
from django.utils.deprecation import MiddlewareMixin

from .conf import settings
from . import serializers
from . import utils



class IamheadlessPublisherAdminAuthenticationMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        token = utils.get_request_user_token(request)

        if token is not None:

            client = utils.get_client()

            req = client.get_user_for_token(
                request=request,
                token=token
            )

            project_id = utils.get_request_project_id(request)

            if req.is_authenticated is True and project_id is not None:
                req.permissions = client.get_user_project_permissions(
                    project_id=project_id,
                    user_id=req.id,
                    token=token,
                )

            setattr(
                request,
                settings.REQUEST_USER_KEY,
                req
            )

        else:

            setattr(
                request,
                settings.REQUEST_USER_KEY,
                serializers.IamheadlessAdminBaseUserSerializer()
            )
