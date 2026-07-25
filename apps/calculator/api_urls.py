from django.urls import path

from .api_views import LoanHistoryAPI

urlpatterns = [
    path(
        "history/",
        LoanHistoryAPI.as_view(),
        name="api_history",
    ),
]