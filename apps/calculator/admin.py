from django.contrib import admin

from .models import LoanCalculation


@admin.register(LoanCalculation)
class LoanCalculationAdmin(admin.ModelAdmin):

    list_display = (
        "loan_amount",
        "annual_interest_rate",
        "loan_tenure",
        "monthly_emi",
        "created_at",
    )

    list_filter = (
        "tenure_type",
        "created_at",
    )

    search_fields = (
        "loan_amount",
    )

    ordering = (
        "-created_at",
    )