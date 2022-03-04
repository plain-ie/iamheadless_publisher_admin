from django.conf import settings as dj_settings

from .apps import IamheadlessPublisherAdminConfig
from .loader import load


class Settings:

    _API_CLIENT = None
    _ITEM_TYPE_REGISTRY = None

    APP_NAME = IamheadlessPublisherAdminConfig.name
    VAR_PREFIX = APP_NAME.upper()

    VAR_ALLOWED_PROJECT_IDS = f'{VAR_PREFIX}_ALLOWED_PROJECT_IDS'
    VAR_API_CLIENT = f'{VAR_PREFIX}_API_CLIENT'
    VAR_API_URL = f'{VAR_PREFIX}_API_URL'
    VAR_DEFAULT_LANGUAGE = f'{VAR_PREFIX}_DEFAULT_LANGUAGE'
    VAR_FILE_HANDLING_BACKEND_CLASS = f'{VAR_PREFIX}_FILE_HANDLING_BACKEND_CLASS'
    VAR_ITEM_TYPE_REGISTRY_CLASS = f'{VAR_PREFIX}_ITEM_TYPE_REGISTRY_CLASS'
    VAR_LANGUAGES = f'{VAR_PREFIX}_LANGUAGES'
    VAR_SERIALIZER_LIST = f'{VAR_PREFIX}_SERIALIZER_LIST'
    VAR_PROJECT_TITLE = f'{VAR_PREFIX}_PROJECT_TITLE'

    REQUEST_USER_KEY = 'iamheadless_publisher_admin_user'

    URLNAME_ITEM_CREATE_STEP_ONE = 'admin-create-items-step-one'
    URLNAME_ITEM_CREATE_STEP_TWO = 'admin-create-items-step-two'
    URLNAME_ITEM_CREATE_STEP_THREE = 'admin-create-items-step-three'
    URLNAME_DASHBOARD = 'admin-dashboard'
    URLNAME_ITEM_DELETE = 'admin-delete-item'
    URLNAME_HOMEPAGE = 'admin-homepage'
    URLNAME_ITEM = 'admin-edit-items'
    URLNAME_ITEMS = 'admin-list-items'
    URLNAME_PROJECTS = 'admin-projects'
    URLNAME_REQUEST_PASSWORD_RESET_LINK = 'admin-request-password-reset-link'
    URLNAME_RESET_PASSWORD = 'admin-reset-password'
    URLNAME_SIGN_IN = 'admin-sign-in'
    URLNAME_SIGN_OUT = 'admin-sign-out'

    @property
    def API_CLIENT(self):

        if self._API_CLIENT is not None:
            return self._API_CLIENT

        client = getattr(
            dj_settings,
            self.VAR_API_CLIENT,
            'iamheadless_publisher_admin.clients.ModelClient'
        )

        self._API_CLIENT = load(client)()

        return self._API_CLIENT

    @property
    def API_URL(self):
        return getattr(dj_settings, self.VAR_API_URL, None)

    @property
    def ALLOWED_PROJECT_IDS(self):
        return getattr(dj_settings, self.VAR_ALLOWED_PROJECT_IDS, [])

    @property
    def DEFAULT_LANGUAGE(self):
        return getattr(dj_settings, self.VAR_DEFAULT_LANGUAGE, None)

    @property
    def FILE_HANDLING_BACKEND_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_FILE_HANDLING_BACKEND_CLASS,
            'iamheadless_publisher_admin.file_handling.LocalFileUploadBackend'
        )

    @property
    def ITEM_TYPE_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_ITEM_TYPE_REGISTRY_CLASS,
            'iamheadless_publisher_admin.registry.ItemTypeRegistry'
        )

    @property
    def ITEM_TYPE_REGISTRY(self):
        if self._ITEM_TYPE_REGISTRY is not None:
            return self._ITEM_TYPE_REGISTRY
        self._ITEM_TYPE_REGISTRY = load(self.ITEM_TYPE_REGISTRY_CLASS)()
        return self._ITEM_TYPE_REGISTRY

    @property
    def LANGUAGES(self):
        return getattr(dj_settings, self.VAR_LANGUAGES, None)

    @property
    def PROJECT_TITLE(self):
        return getattr(dj_settings, self.VAR_PROJECT_TITLE, '')

    @property
    def SERIALIZER_LIST(self):
        return getattr(dj_settings, self.VAR_SERIALIZER_LIST, [])

    @property
    def RESET_LINK_MAX_AGE(self):
        return 60 * 15

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
