from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import reverse
from django.utils.dateparse import parse_datetime

from .conf import settings


class IamheadlessAdminBaseUserSerializer:

    email = None
    is_authenticated = False
    first_name = None
    last_name = None
    permissions = None
    token=None

    def __init__(
            self,
            id=None,
            first_name=None,
            last_name=None,
            email=None,
            is_authenticated=False,
            permissions=None,
            token=None,
            ):

        self.id = id
        self.email = email
        self.is_authenticated = is_authenticated
        self.first_name = first_name
        self.last_name = last_name
        self.permissions = permissions
        self.token=token

    @property
    def data(self):
        return {
            'id': id,
            'email': email,
            'is_authenticated': is_authenticated,
            'first_name': first_name,
            'last_name': last_name,
            'permissions': permissions,
            'token': token,
        }

    def get_user_tenant_ids(
            self,
            project_ids=None
            ):

        cleaned_project_ids = None
        tenants = []

        if isinstance(project_ids, list) is False and project_ids is not None:
            project_ids = [project_ids, ]

        if isinstance(project_ids, list) is True:
            cleaned_project_ids = []
            for x in project_ids:
                if isinstance(x, str) is False:
                    x = str(x)
                cleaned_project_ids.append(x)

        for project_id in self.permissions.keys():

            project = self.permissions[project_id]

            if isinstance(project, str) is True:
                _tenants = ['*']
            elif isinstance(project, dict) is True:
                _tenants = list(project.keys())
            else:
                raise ValueError('Expected str or list')

            if len(_tenants) != 0:
                if cleaned_project_ids is not None:
                    if project_id in cleaned_project_ids:
                        tenants += _tenants
                else:
                    tenants += _tenants

        return tenants

    def is_project_admin(
            self,
            project_id,
            ):

        if isinstance(project_id, str) is False:
            project_id = str(project_id)

        value = None

        try:
            value = self.permissions[project_id]
        except KeyError:
            return False

        return value == '*'

    def is_project_user(
            self,
            project_id
            ):

        if isinstance(project_id, str) is False:
            project_id = str(project_id)

        return self.get_user_tenants(project_id) != 0


class IamheadlessAdminAnonymousUserSerializer(IamheadlessAdminBaseUserSerializer):
    pass


class IamheadlessAdminUserSerializer(IamheadlessAdminBaseUserSerializer):

    is_authenticated = True

    def __init__(
            self,
            id=None,
            first_name=None,
            last_name=None,
            email=None,
            permissions=None,
            token=None,
            ):

        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.permissions = permissions
        self.token=token
