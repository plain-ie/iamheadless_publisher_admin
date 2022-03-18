from django.urls import include, path

from .conf import settings
from .viewsets.authentication import ResetPasswordViewSet, RequestPasswordResetLinkViewSet, SignInViewSet, SignOutViewSet
from .viewsets.item import ItemCreationWorkFlowStepOne, ItemCreationWorkFlowStepTwo, ItemCreationWorkFlowStepThree
from .viewsets.items import ItemListViewSet
from .viewsets.homepage import DashboardViewSet, HomepageViewSet
from .viewsets.projects import ProjectsViewSet

from iamheadless_readability.viewsets import ReadabilityViewSet


urlpatterns = [

    # ----
    path('', include(settings.VIEWSET_REGISTRY.get_urlpatterns(prefix=settings.URL_PREFIX))),

    # --- Tools ---
    path(rf'{settings.URL_PREFIX}tools/text-analyzer/', ReadabilityViewSet.as_view(), name=settings.URLNAME_READABILITY_TEXT_ANALYZE),

    # --- Items Create ---
    path(rf'{settings.URL_PREFIX}projects/<str:project_id>/tenants/<str:tenant_id>/item-types/<str:item_type>/', ItemCreationWorkFlowStepThree.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_THREE),
    path(rf'{settings.URL_PREFIX}projects/<str:project_id>/item-types/<str:item_type>/', ItemCreationWorkFlowStepThree.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_THREE),
    path(rf'{settings.URL_PREFIX}projects/<str:project_id>/select-tenant/item-type/<str:item_type>/', ItemCreationWorkFlowStepTwo.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_TWO),
    path(rf'{settings.URL_PREFIX}projects/<str:project_id>/select-item-type/', ItemCreationWorkFlowStepOne.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_ONE),

    # --- Items List ---
    path(rf'{settings.URL_PREFIX}projects/<str:project_id>/items/', ItemListViewSet.as_view(), name=settings.URLNAME_ITEMS),

    # --- Dashboard ---
    # path(rf'{settings.URL_PREFIX}projects/<str:project_id>/', DashboardViewSet.as_view(), name=settings.URLNAME_DASHBOARD),
    path(rf'{settings.URL_PREFIX}projects/', ProjectsViewSet.as_view(), name=settings.URLNAME_PROJECTS),

    # --- Authentication ---
    path(rf'{settings.URL_PREFIX}authentication/sign-in/', SignInViewSet.as_view(), name=settings.URLNAME_SIGN_IN),
    path(rf'{settings.URL_PREFIX}authentication/sign-out/', SignOutViewSet.as_view(), name=settings.URLNAME_SIGN_OUT),
    path(rf'{settings.URL_PREFIX}authentication/reset-password/<str:token>/', ResetPasswordViewSet.as_view(), name=settings.URLNAME_RESET_PASSWORD),
    path(rf'{settings.URL_PREFIX}authentication/reset-password/', RequestPasswordResetLinkViewSet.as_view(), name=settings.URLNAME_REQUEST_PASSWORD_RESET_LINK),

    path(rf'{settings.URL_PREFIX}', HomepageViewSet.as_view(), name=settings.URLNAME_HOMEPAGE),

]
