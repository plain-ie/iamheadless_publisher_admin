from django.urls import path

from . import permissions
from . import utils


class ItemViewSetPermissionMixin:

    def has_access(self):
        permissions.user_can_access_item_type(
            self.get_request_user(),
            self.get_project_id(),
            self.get_item_type()
        )


class UtilsViewSetMixin:

    def get_client(self):
        return utils.get_client()

    def get_project_id(self):
        return utils.get_request_project_id(self.request)

    def get_tenant_id(self):
        return utils.get_request_tenant_id(self.request)

    def get_item_id(self):
        return utils.get_request_item_id(self.request)

    def get_item_type(self):
        item_type = utils.get_request_item_type(self.request)
        if item_type is not None:
            return item_type
        return getattr(self, 'item_type', None)

    def get_request_user_token(self):
        return utils.get_request_user_token(self.request)

    def get_request_user(self):
        return utils.get_request_user(self.request)

    def get_item_type_serializer(self, item_type=None):
        if item_type is not None:
            return utils.get_item_type_serializer(item_type)
        return self.pydantic_model
