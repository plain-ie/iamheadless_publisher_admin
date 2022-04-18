import json

from django.core.serializers import serialize

from .conf import settings
from . import serializers
from . import pydantic_models


class BaseClient:

    def __init__(self, *args, **kwargs):
        self.dependencies_check()

    def dependencies_check(self):
        pass


class ApiClient(BaseClient):

    API_URL = settings.API_URL

    def dependencies_check(self):
        if self.API_URL is None:
            raise ValueError('API_URL cannot be None')


class ModelClient(BaseClient):

    def dependencies_check(self):
        pass

    # Authenticate

    def sign_in(self, request, username, password):

        from django.contrib.auth import authenticate as dj_authenticate
        from django.contrib.auth import login as dj_login
        from django.contrib.auth import get_user as dj_get_user

        user = dj_authenticate(request, username=username, password=password)
        if user is None:
            return None

        dj_login(request, user)

        return serializers.IamheadlessAdminUserSerializer(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            permissions={},
            token=None,
        )

    def sign_out(self, request):
        from django.contrib.auth import logout
        logout(request)
        return None

    def send_reset_link(self, email, reset_link):
        return None

    def reset_password(self, email, password):
        from iamheadless_projects.lookups.user import change_user_password
        return change_user_password(email, password)

    # Projects

    def publishing_projects(
            self,
            project_ids=None,
            token=None,
            ):

            # XXXX TODO

        return []

    # User

    def get_user_for_token(
            self,
            request=None,
            token=None,
            ):

        from django.contrib.auth import get_user as dj_get_user

        user = dj_get_user(request)

        if user.is_authenticated is False:
            return serializers.IamheadlessAdminAnonymousUserSerializer()

        permissions = None

        return serializers.IamheadlessAdminUserSerializer(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            permissions=permissions,
            token=token,
        )

    def get_user_project_permissions(
            self,
            project_id,
            user_id,
            token=None,
            ):

        from iamheadless_projects.lookups.user_permissions import get_user_permissions

        return get_user_permissions(user_id, [project_id])

    # Permissions

    def project_admins(
            self,
            project_id,
            count=10,
            page=1,
            token=None,
            user_ids=None,
            ):

        from iamheadless_projects.lookups.project_admins import get_project_admins

        return get_project_admins(
            project_id,
            count=count,
            page=page,
            user_ids=user_ids,
            format='dict',
        )

    def project_users(
            self,
            project_id,
            count=10,
            page=1,
            token=None,
            user_ids=None
            ):

        from iamheadless_projects.lookups.project_users import get_project_users

        return get_project_users(
            project_id,
            count=count,
            page=page,
            user_ids=user_ids,
            format='dict',
        )

    def project_tenants(
            self,
            project_id,
            count=10,
            page=1,
            tenant_ids=None,
            token=None,
            ):

        from iamheadless_projects.lookups.project_tenants import get_project_tenants

        return get_project_tenants(
            project_id,
            count=count,
            page=page,
            tenant_ids=tenant_ids,
            format='dict',
        )

    def project_tenant(
            self,
            project_id,
            tenant_id,
            token=None,
            ):

        from iamheadless_projects.lookups.tenant import get_tenant

        return get_tenant(
            tenant_id,
            project_id=project_id,
            format='dict',
        )

    def tenant_users(
            self,
            tenant_id,
            count=10,
            page=1,
            token=None,
            user_ids=None,
            ):

        from iamheadless_projects.lookups.tenant_users import get_tenant_users

        return get_tenant_users(
            tenant_id,
            count=count,
            page=page,
            user_ids=user_ids,
            format='dict',
        )

    #

    def retrieve_items(
            self,
            project_id,
            count=10,
            item_type=None,
            page=1,
            published=None,
            tenant_id=None,
            token=None,
            unpublished=None,
            ):

        from iamheadless_publisher.lookups.items_retrieve import retrieve_items as publisher_retrieve_items
        from iamheadless_publisher.pydantic_models import NestedItemSchema

        data = publisher_retrieve_items(
            count=count,
            item_ids=None,
            item_types=item_type,
            project_ids=project_id,
            page=page,
            published=published,
            tenant_ids=tenant_id,
            unpublished=unpublished,
            format='dict',
            item_pydantic_model=NestedItemSchema,
        )

        # data = json.loads(data)

        data['results'] = settings.ITEM_TYPE_REGISTRY.serialize(data['results'])

        return data

    # CRUD

    def create_item(
            self,
            project_id,
            tenant_id,
            item_type,
            data,
            token=None,
            ):

        from iamheadless_publisher.lookups.item_create import create_item as publisher_create_item

        data = data
        data['project_id'] = project_id
        data['tenant_id'] = tenant_id
        data['item_type'] = item_type

        instance = publisher_create_item(data, format='dict')

        data['id'] = instance['id']

        return data

    def delete_item(
            self,
            item_id,
            project_id=None,
            tenant_id=None,
            token=None,
            ):

        from iamheadless_publisher.lookups.item_delete import delete_item as publisher_delete_item

        return publisher_delete_item(item_id)

    def retrieve_item(
            self,
            item_id,
            project_id=None,
            tenant_id=None,
            token=None,
            ):

        from iamheadless_publisher.lookups.item_retrieve import retrieve_item as publisher_retrieve_item
        from iamheadless_publisher.pydantic_models import ItemSchema, NestedItemSchema

        instance = publisher_retrieve_item(
            item_id,
            format='dict',
            item_pydantic_model=ItemSchema,
            nested_item_pydantic_model=NestedItemSchema,
        )

        return instance

    def update_item(
            self,
            item_id,
            data,
            project_id=None,
            tenant_id=None,
            token=None,
            ):

        from iamheadless_publisher.lookups.item_update import update_item as publisher_update_item

        instance = publisher_update_item(item_id, data, format='dict')

        return instance
