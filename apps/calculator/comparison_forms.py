from django import forms


class LoanComparisonForm(forms.Form):
    loan_amount = forms.DecimalField(
        label="Loan Amount",
        min_value=1,
        decimal_places=2,
        max_digits=12,
    )

    interest_rate_1 = forms.DecimalField(
        label="Interest Rate (Loan A)",
        decimal_places=2,
        max_digits=5,
    )

    interest_rate_2 = forms.DecimalField(
        label="Interest Rate (Loan B)",
        decimal_places=2,
        max_digits=5,
    )

    tenure = forms.IntegerField(
        label="Tenure (Months)",
        min_value=1,
    )