from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "history/",
        views.history,
        name="history",
    ),

    path(
        "export/excel/",
        views.export_excel,
        name="export_excel",
    ),

    path(
        "calculation/<int:pk>/",
        views.calculation_detail,
        name="calculation_detail",
    ),

    path(
        "calculation/<int:pk>/delete/",
        views.delete_calculation,
        name="delete_calculation",
    ),

    path(
        "export/<int:pk>/",
        views.export_pdf,
        name="export_pdf",
    ),

    path(
        "compare/",
        views.compare_loans,
        name="compare_loans",
    ),

    path(
        "schedule/<int:pk>/",
        views.amortization_schedule,
        name="amortization_schedule",
    ),

    path(
        "eligibility/",
        views.loan_eligibility,
        name="loan_eligibility",
    ),

    path(
        "prepayment/",
        views.prepayment,
        name="prepayment",
    ),
]