from django.core.exceptions import PermissionDenied

from .conf import settings


def user_can_access_item_type(user, project_id, item_type):

    user_is_project_admin = user.is_project_admin(project_id)

    types = settings.ITEM_TYPE_REGISTRY.get_item_types(
        for_admin=user_is_project_admin,
        item_types=[item_type, ]
    )

    if len(types) == 0:

        raise PermissionDenied(
            f'User "{user.id}" does not have access to item type "{item_type}"'
        )

    pass
