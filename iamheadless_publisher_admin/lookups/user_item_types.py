from ..conf import settings


def get_user_item_types(
        user,
        types=None
        ):

    if isinstance(types, list) is False and types is not None:
        types = [types, ]

    registry = settings.ITEM_TYPE_REGISTRY
    user_is_project_admin = False

    item_types = []

    for key in registry.item_types.keys():

        proceed = True

        if types is not None:
            if key not in types:
                proceed = False

        if proceed is True:
            serializer = registry.item_types[key]
            requires_admin = getattr(
                serializer,
                'project_admin_required',
                False
            )

            if requires_admin is True and user_is_project_admin is True:
                item_types.append(serializer)

            elif requires_admin is False:
                item_types.append(serializer)

    return item_types
