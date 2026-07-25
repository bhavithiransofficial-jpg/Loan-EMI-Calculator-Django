from django import forms
from .constants import TENURE_CHOICES


class LoanCalculatorForm(forms.Form):
    loan_amount = forms.DecimalField(
        label="Loan Amount (₹)",
        min_value=1,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 500000",
            }
        ),
    )

    annual_interest_rate = forms.DecimalField(
        label="Annual Interest Rate (%)",
        min_value=0.01,
        max_value=100,
        decimal_places=2,
        max_digits=5,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 8.5",
            }
        ),
    )

    loan_tenure = forms.IntegerField(
        label="Loan Tenure",
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 5",
            }
        ),
    )

    tenure_type = forms.ChoiceField(
        label="Tenure Type",
        choices=TENURE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )