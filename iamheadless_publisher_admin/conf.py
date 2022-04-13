from django.conf import settings as dj_settings

from .apps import IamheadlessPublisherAdminConfig as AppConfig
from .loader import load


class Settings:

    _API_CLIENT = None
    _ITEM_TYPE_REGISTRY = None
    _VIEWSET_REGISTRY = None

    APP_NAME = AppConfig.name
    VAR_PREFIX = APP_NAME.upper()

    VAR_ALLOWED_PROJECT_IDS = f'{VAR_PREFIX}_ALLOWED_PROJECT_IDS'
    VAR_API_CLIENT = f'{VAR_PREFIX}_API_CLIENT'
    VAR_API_URL = f'{VAR_PREFIX}_API_URL'
    VAR_DEFAULT_LANGUAGE = f'{VAR_PREFIX}_DEFAULT_LANGUAGE'
    VAR_FILE_HANDLING_BACKEND_CLASS = f'{VAR_PREFIX}_FILE_HANDLING_BACKEND_CLASS'
    VAR_HANDLER_403 = f'{VAR_PREFIX}_HANDLER_403'
    VAR_HANDLER_404 = f'{VAR_PREFIX}_HANDLER_404'
    VAR_HANDLER_500 = f'{VAR_PREFIX}_HANDLER_500'
    VAR_ITEM_TYPE_REGISTRY_CLASS = f'{VAR_PREFIX}_ITEM_TYPE_REGISTRY_CLASS'
    VAR_ITEMS_LIST_LENGTH = f'{VAR_PREFIX}_ITEMS_LIST_LENGTH'
    VAR_LANGUAGES = f'{VAR_PREFIX}_LANGUAGES'
    VAR_SERIALIZER_CLASS = f'{VAR_PREFIX}_SERIALIZER_REGISTRY_CLASS'
    VAR_SERIALIZER_LIST = f'{VAR_PREFIX}_SERIALIZER_LIST'
    VAR_PROJECT_TITLE = f'{VAR_PREFIX}_PROJECT_TITLE'
    VAR_URL_PREFIX = f'{VAR_PREFIX}_URL_PREFIX'
    VAR_VIEWSET_REGISTRY_CLASS = f'{VAR_PREFIX}_VIEWSET_REGISTRY_CLASS'

    REQUEST_USER_KEY = 'iamheadless_publisher_admin_user'

    URLNAME_ITEM_CREATE_STEP_ONE = 'admin-create-items-step-one'
    URLNAME_ITEM_CREATE_STEP_TWO = 'admin-create-items-step-two'
    URLNAME_ITEM_CREATE_STEP_THREE = 'admin-create-items-step-three'
    URLNAME_DASHBOARD = 'admin-dashboard'
    URLNAME_ITEM_DELETE = 'admin-delete-item'
    URLNAME_HOMEPAGE = 'admin-homepage'
    URLNAME_ITEMS = 'admin-list-items'
    URLNAME_PROJECTS = 'admin-projects'
    URLNAME_READABILITY_TEXT_ANALYZE = 'text-analyzer'
    URLNAME_REQUEST_PASSWORD_RESET_LINK = 'admin-request-password-reset-link'
    URLNAME_RESET_PASSWORD = 'admin-reset-password'
    URLNAME_SIGN_IN = 'admin-sign-in'
    URLNAME_SIGN_OUT = 'admin-sign-out'

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
    def LANGUAGES(self):
        return getattr(dj_settings, self.VAR_LANGUAGES, None)

    @property
    def PROJECT_TITLE(self):
        return getattr(dj_settings, self.VAR_PROJECT_TITLE, '')

    @property
    def RESET_LINK_MAX_AGE(self):
        return 60 * 15

    @property
    def URL_PREFIX(self):
        return getattr(dj_settings, self.VAR_URL_PREFIX, 'cms/')

    @property
    def ITEMS_LIST_LENGTH(self):
        return getattr(
            dj_settings,
            self.VAR_ITEMS_LIST_LENGTH,
            10
        )

    #

    @property
    def HANDLER_403(self):
        return getattr(
            dj_settings,
            self.VAR_HANDLER_403,
            'iamheadless_publisher_admin.viewsets.error_handling.handler403'
        )

    @property
    def HANDLER_404(self):
        return getattr(
            dj_settings,
            self.VAR_HANDLER_404,
            'iamheadless_publisher_admin.viewsets.error_handling.handler404'
        )

    @property
    def HANDLER_500(self):
        return getattr(
            dj_settings,
            self.VAR_HANDLER_500,
            'iamheadless_publisher_admin.viewsets.error_handling.handler500'
        )

    #

    @property
    def API_CLIENT(self):

        if self._API_CLIENT is not None:
            return self._API_CLIENT

        client = getattr(
            dj_settings,
            self.VAR_API_CLIENT,
            f'{self.APP_NAME}.clients.ModelClient'
        )

        self._API_CLIENT = load(client)()

        return self._API_CLIENT

    #

    @property
    def FILE_HANDLING_BACKEND_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_FILE_HANDLING_BACKEND_CLASS,
            f'{self.APP_NAME}.file_handling.LocalFileUploadBackend'
        )

    #

    @property
    def ITEM_TYPE_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_ITEM_TYPE_REGISTRY_CLASS,
            f'{self.APP_NAME}.registry.ItemTypeRegistry'
        )

    @property
    def ITEM_TYPE_REGISTRY(self):
        if self._ITEM_TYPE_REGISTRY is not None:
            return self._ITEM_TYPE_REGISTRY
        self._ITEM_TYPE_REGISTRY = load(self.ITEM_TYPE_REGISTRY_CLASS)()
        return self._ITEM_TYPE_REGISTRY

    #

    @property
    def SERIALIZER_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_SERIALIZER_CLASS,
            f'{self.APP_NAME}.registry.ItemTypeRegistry'
        )

    @property
    def SERIALIZER_LIST(self):
        return getattr(dj_settings, self.VAR_SERIALIZER_LIST, [])

    #

    @property
    def VIEWSET_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            self.VAR_VIEWSET_REGISTRY_CLASS,
            f'{self.APP_NAME}.registry.ViewSetRegistry'
        )

    @property
    def VIEWSET_REGISTRY(self):
        if self._VIEWSET_REGISTRY is not None:
            return self._VIEWSET_REGISTRY
        self._VIEWSET_REGISTRY = load(self.VIEWSET_REGISTRY_CLASS)()
        return self._VIEWSET_REGISTRY

    # def __getattr__(self, name):
    #     return getattr(dj_settings, name)


settings = Settings()
