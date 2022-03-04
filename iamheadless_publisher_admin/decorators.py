from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse

from .conf import settings
from . import utils


def login_required(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            url = reverse(settings.URLNAME_SIGN_IN)
            url += '?next=' + request.build_absolute_uri()
            response = redirect(url)

            user = utils.get_request_user(request)

            if user is None:
                return response

            if user.is_authenticated is False:
                return response

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator


def unauthenticated_user_required(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            url = reverse(settings.URLNAME_PROJECTS)
            response = redirect(url)

            user = utils.get_request_user(request)

            if user is not None:
                if user.is_authenticated is True:
                    return response

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator


def user_has_project_access(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            user = utils.get_request_user(request)
            project_id = utils.get_request_project_id(request)

            if user is None:
                raise PermissionDenied('Authentication required')

            try:
                project = user.permissions[str(project_id)]
            except KeyError:
                raise PermissionDenied(
                    f'User "{user.id}" does not have access to project "{project_id}"'
                )

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator


def user_has_tenant_access(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            user = utils.get_request_user(request)
            project_id = utils.get_request_project_id(request)
            tenant_id = utils.get_request_tenant_id(request)

            if tenant_id is not None:
                tenant_ids = user.get_user_tenant_ids(project_id)

                if str(tenant_id) not in tenant_ids and '*' not in tenant_ids:
                    raise PermissionDenied(
                        f'User "{user.id}" does not have access to tentant "{tenant_id}"'
                    )

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator


def user_has_item_type_access(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            user = utils.get_request_user(request)
            project_id = utils.get_request_project_id(request)
            item_type = utils.get_request_item_type(request)

            if user is None:
                raise PermissionDenied('Authentication required')

            user_is_project_admin = user.is_project_admin(project_id)

            types = settings.ITEM_TYPE_REGISTRY.get_item_types(
                for_admin=user_is_project_admin,
                item_types=[item_type, ]
            )

            if len(types) == 0:
                raise PermissionDenied(
                    f'User "{user.id}" does not have access to item type "{item_type}"'
                )

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator


def tenant_has_project_access(*args, **kwargs):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):

            project_id = utils.get_request_project_id(request)
            tenant_id = utils.get_request_tenant_id(request)

            if tenant_id is not None:
                if utils.tenant_is_project_tenant(request, project_id, tenant_id) is False:
                    raise PermissionDenied(
                        f'Tenant "{tenant_id}" does not have access to project "{project_id}"'
                    )

            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
