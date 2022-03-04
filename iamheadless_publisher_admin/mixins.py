from . import utils


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
        return utils.get_request_item_type(self.request)

    def get_request_user_token(self):
        return utils.get_request_user_token(self.request)

    def get_request_user(self):
        return utils.get_request_user(self.request)

    def get_item_type_serializer(self, item_type):
        return utils.get_item_type_serializer(item_type)
