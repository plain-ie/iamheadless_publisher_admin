import datetime
from typing import List, Optional

from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from pydantic import BaseModel, Field

from .conf import settings


class BaseUser(BaseModel):
    email: str
    first_name: Optional[str] = None
    id: str
    is_authenticated: bool
    last_name: Optional[str] = None
    permissions: Optional[dict] = None
    token: str


class AnonymousUser(BaseUser):
    email: Optional[str] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    is_authenticated: Optional[bool]
    last_name: Optional[str] = None
    permissions: Optional[dict] = None
    token: Optional[str] = None


class Project(BaseModel):
    id: str
    name: str


class Tenant(BaseModel):
    id: str
    name: str


class BaseItemContentsPydanticModel(BaseModel):

    @classmethod
    def get_language(cls, data):
        return data['language']


class BaseItemDataPydanticModel(BaseModel):
    pass

class BaseItemPydanticModel(BaseModel):

    _content_model = BaseItemContentsPydanticModel
    _data_model = BaseItemDataPydanticModel
    _display_name_plural = None
    _display_name_singular = None
    _item_type = None
    _max_per_project = 0
    _max_per_tenant = 0
    _primary_language = settings.DEFAULT_LANGUAGE[0]
    _project_admin_required = False
    _secondary_language=None
    _tenant_required = False

    #
    id: Optional[str]
    #
    item_type: str
    data: _data_model
    #
    project: str
    tenant: Optional[str]
    #
    updated_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]

    @property
    def DATA(self):
        return self.dict()

    @property
    def ITEM_TYPE(self):
        return self._display_name_singular

    @property
    def TITLE(self):
        return None

    @property
    def EDIT_URL(self):

        _data = self.DATA

        project_id = _data.get('project', None)
        tenant_id = _data.get('tenant', None)
        item_id = _data.get('id', None)

        kwargs = {
            'item_type': self._item_type
        }

        if project_id is not None:
            kwargs['project_id'] = project_id

        if tenant_id is not None:
            kwargs['tenant_id'] = tenant_id

        if item_id is not None:
            kwargs['item_id'] = item_id

        return reverse(
            settings.URLNAME_ITEM,
            kwargs=kwargs
        )

    #

    @classmethod
    def viewsets(cls):
        return []

    @classmethod
    def get_item_type(cls, data):
        return data.get('item_type', None)

    @classmethod
    def get_display_content(
            cls,
            contents,
            requested_language,
            ):

        _contents = {}

        primary_content = None
        secondary_content = None

        # Change list to dict
        for content in contents:
            language = cls._content_model.get_language(content)
            _contents[language] = content

        try:
            primary_content = _contents[cls._primary_language]
        except KeyError:
            pass

        if cls._secondary_language is not None:
            try:
                secondary_content = _contents[cls._secondary_language]
            except KeyError:
                pass

        try:
            return _contents[requested_language]
        except KeyError:
            pass

        if primary_content is None and secondary_content is None:
            raise ValidationError('No content to display')

        if primary_content is None:
            return secondary_content

        return primary_content

    @classmethod
    def render_form(cls, request, initial_data):
        return ''

    @classmethod
    def validate_form(cls, request, initial_data):
        return ''

    # PRE

    @classmethod
    def pre_create(cls, request, data):
        return data

    @classmethod
    def pre_delete(cls, request, data):
        return data

    @classmethod
    def pre_update(cls, request, data):
        return data

    # POST

    @classmethod
    def post_create(cls, request, data):
        return data

    @classmethod
    def post_delete(cls, request, data):
        return data

    @classmethod
    def post_update(cls, request, data):
        return data
