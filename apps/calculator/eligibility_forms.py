from django import forms


class LoanEligibilityForm(forms.Form):

    monthly_income = forms.DecimalField(
        label="Monthly Income (₹)",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    monthly_expenses = forms.DecimalField(
        label="Monthly Expenses (₹)",
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    annual_interest_rate = forms.DecimalField(
        label="Interest Rate (%)",
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    tenure = forms.IntegerField(
        label="Loan Tenure (Months)",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )