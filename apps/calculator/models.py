from django.db import models
from django.contrib.auth.models import User


class LoanCalculation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="loan_calculations",
        null=True,
        blank=True,
    )

    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    annual_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    loan_tenure = models.PositiveIntegerField()

    tenure_type = models.CharField(
        max_length=10,
    )

    monthly_emi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_interest = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # NEW FIELD
    schedule = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"₹{self.loan_amount} | "
            f"{self.loan_tenure} {self.tenure_type}"
        )