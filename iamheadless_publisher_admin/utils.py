from django.conf import settings as dj_settings

from .conf import settings
from .loader import load


def get_client():
    return settings.API_CLIENT


#

def get_request_project_id(request):
    return request.resolver_match.kwargs.get('project_id', None)


def get_request_tenant_id(request):
    return request.resolver_match.kwargs.get('tenant_id', None)


def get_request_item_type(request):
    return request.resolver_match.kwargs.get('item_type', None)


def get_request_item_id(request):
    return request.resolver_match.kwargs.get('item_id', None)


#

def get_session_cookie_name():
    return dj_settings.SESSION_COOKIE_NAME

def get_request_user_token(request):
    return request.COOKIES.get(get_session_cookie_name(), None)


def get_request_user(request):
    return getattr(request, settings.REQUEST_USER_KEY, None)


#


def get_item_type_serializer(item_type):
    return settings.ITEM_TYPE_REGISTRY.find(item_type)


#

def tenant_is_project_tenant(request, project_id, tenant_id):

    # TODO
    # CACHE THIS FOR X SEC

    req = get_client().project_tenants(
        project_id,
        tenant_ids=[tenant_id, ],
        count=1,
        page=1,
        token=get_request_user_token(request),
    )

    return len(req.get('results', [])) == 1


def get_user_tenants_choices(project_id, user):

    tenant_ids = user.get_user_tenant_ids(project_id)

    if tenant_ids is not None:

        if len(tenant_ids) == 0:
            tenant_ids = None

        if '*' in tenant_ids:
            tenant_ids = None

    req = get_client().project_tenants(
        project_id=project_id,
        tenant_ids=tenant_ids,
        count=1000000000,
        page=1,
    )

    results = req['results']

    choices = []

    for x in results:
        choices.append([
            x['id'],
            x['name']
        ])

    # XXXX TODO: sort choices

    return choices


def get_user_item_types_choices(project_id, user):

    user_is_project_admin = user.is_project_admin(project_id)

    choices = settings.ITEM_TYPE_REGISTRY.get_item_types(
        for_admin=user_is_project_admin,
        format='choices'
    )

    # XXXX TODO: sort choices

    return choices


def get_file_handling_backend():
    return load(settings.FILE_HANDLING_BACKEND_CLASS)
