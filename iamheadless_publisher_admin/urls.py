from django.urls import path

from .conf import settings
from .viewsets.authentication import ResetPasswordViewSet, RequestPasswordResetLinkViewSet, SignInViewSet, SignOutViewSet
from .viewsets.item import ItemViewSet, ItemCreationWorkFlowStepOne, ItemCreationWorkFlowStepTwo, ItemCreationWorkFlowStepThree, ItemDeleteViewSet
from .viewsets.items import ItemListViewSet
from .viewsets.homepage import DashboardViewSet, HomepageViewSet
from .viewsets.projects import ProjectsViewSet

from iamheadless_readablility.viewsets import ReadabilityViewSet


URL_PREFIX = 'cms/'


urlpatterns = [

    # --- Items Delete ---
    path(rf'{URL_PREFIX}tools/text-analyzer/', ReadabilityViewSet.as_view(), name=settings.URLNAME_READABILITY_TEXT_ANALYZE),

    # --- Items Delete ---
    path(rf'{URL_PREFIX}projects/<str:project_id>/tenants/<str:tenant_id>/item-types/<str:item_type>/items/<str:item_id>/delete/', ItemDeleteViewSet.as_view(), name=settings.URLNAME_ITEM_DELETE),
    path(rf'{URL_PREFIX}projects/<str:project_id>/item-types/<str:item_type>/items/<str:item_id>/delete/', ItemDeleteViewSet.as_view(), name=settings.URLNAME_ITEM_DELETE),

    # --- Items Get/Update ---
    path(rf'{URL_PREFIX}projects/<str:project_id>/tenants/<str:tenant_id>/item-types/<str:item_type>/items/<str:item_id>/', ItemViewSet.as_view(), name=settings.URLNAME_ITEM),
    path(rf'{URL_PREFIX}projects/<str:project_id>/item-types/<str:item_type>/items/<str:item_id>/', ItemViewSet.as_view(), name=settings.URLNAME_ITEM),

    # --- Items Create ---
    path(rf'{URL_PREFIX}projects/<str:project_id>/tenants/<str:tenant_id>/item-types/<str:item_type>/', ItemCreationWorkFlowStepThree.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_THREE),
    path(rf'{URL_PREFIX}projects/<str:project_id>/item-types/<str:item_type>/', ItemCreationWorkFlowStepThree.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_THREE),
    path(rf'{URL_PREFIX}projects/<str:project_id>/select-tenant/item-type/<str:item_type>/', ItemCreationWorkFlowStepTwo.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_TWO),
    path(rf'{URL_PREFIX}projects/<str:project_id>/select-item-type/', ItemCreationWorkFlowStepOne.as_view(), name=settings.URLNAME_ITEM_CREATE_STEP_ONE),

    # --- Items List ---
    path(rf'{URL_PREFIX}projects/<str:project_id>/items/', ItemListViewSet.as_view(), name=settings.URLNAME_ITEMS),

    # --- Tenants List ---
    # path(rf'{URL_PREFIX}projects/<str:project_id>/tenants/', TenantsListViewSet.as_view(), name='tenants-list'),

    # --- Dashboard ---
    # path(rf'{URL_PREFIX}projects/<str:project_id>/', DashboardViewSet.as_view(), name=settings.URLNAME_DASHBOARD),
    path(rf'{URL_PREFIX}projects/', ProjectsViewSet.as_view(), name=settings.URLNAME_PROJECTS),

    # --- User profile management ---
    # path(rf'{URL_PREFIX}projects/<str:project_id>/profile/', ProjectUserProfileViewSet.as_view(), name='project-user-profile'),
    # path(rf'{URL_PREFIX}profile/', UserProfileViewSet.as_view(), name='user-profile'),

    # --- Authentication ---
    path(rf'{URL_PREFIX}authentication/sign-in/', SignInViewSet.as_view(), name=settings.URLNAME_SIGN_IN),
    path(rf'{URL_PREFIX}authentication/sign-out/', SignOutViewSet.as_view(), name=settings.URLNAME_SIGN_OUT),
    path(rf'{URL_PREFIX}authentication/reset-password/<str:token>/', ResetPasswordViewSet.as_view(), name=settings.URLNAME_RESET_PASSWORD),
    path(rf'{URL_PREFIX}authentication/reset-password/', RequestPasswordResetLinkViewSet.as_view(), name=settings.URLNAME_REQUEST_PASSWORD_RESET_LINK),

    path(rf'{URL_PREFIX}', HomepageViewSet.as_view(), name=settings.URLNAME_HOMEPAGE),

]
