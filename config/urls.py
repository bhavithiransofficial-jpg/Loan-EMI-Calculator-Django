from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("apps.calculator.urls"),
    ),

    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),

    # Calculator API
    path(
        "api/",
        include("apps.calculator.api_urls"),
    ),

    # JWT Authentication
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]