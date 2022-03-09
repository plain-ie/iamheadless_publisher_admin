# iamheadless_publisher_admin

App to render `iamheadless_publisher` frontend.

## Installation

Requires `iamheadless_projects`
Requires `iamheadless_publisher`

1. install package
2. add `iamheadless_publisher_admin` to `INSTALLED_APPS` in `settings.py`
3. add `'iamheadless_publisher_admin.middleware.IamheadlessPublisherAdminAuthenticationMiddleware'` to `MIDDLEWARE` in `settings.py`
4. add `LOGIN_URL = 'sign-in'` to settings.py
5. add `IAMHEADLESS_PUBLISHER_ADMIN_DEFAULT_LANGUAGE = ('en', 'English')` to `settings.py`
6. add `IAMHEADLESS_PUBLISHER_ADMIN_LANGUAGES = (IAMHEADLESS_PUBLISHER_ADMIN_DEFAULT_LANGUAGE, )` to `settings.py`
7. add `IAMHEADLESS_PUBLISHER_ADMIN_ALLOWED_PROJECT_IDS = []` to `settings.py`
8. add `IAMHEADLESS_PUBLISHER_ADMIN_PROJECT_TITLE = 'Iamheadless Publisher Admin'` to `settings.py`
9. add `IAMHEADLESS_PUBLISHER_ADMIN_SERIALIZER_LIST = []` to `settings.py`
10. add `path('', include('iamheadless_publisher_admin.urls'))` to `urlpatterns` in `urls.py`
