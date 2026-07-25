from django import forms


class PrepaymentForm(forms.Form):

    loan_amount = forms.DecimalField(
        label="Loan Amount",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    annual_interest_rate = forms.DecimalField(
        label="Interest Rate (%)",
        min_value=0,
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

    prepayment = forms.DecimalField(
        label="Prepayment Amount",
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )