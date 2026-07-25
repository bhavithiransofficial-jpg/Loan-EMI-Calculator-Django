from decimal import Decimal
from math import pow

from .amortization import AmortizationService


class EMICalculatorService:

    @staticmethod
    def calculate(principal, annual_rate, tenure, tenure_type):
        """
        Calculate EMI and generate amortization schedule.
        """

        principal = Decimal(principal)
        annual_rate = Decimal(annual_rate)

        # Convert tenure to months
        if tenure_type == "years":
            months = tenure * 12
        else:
            months = tenure

        # Monthly interest rate
        monthly_rate = annual_rate / Decimal("1200")

        # EMI calculation
        if monthly_rate == 0:
            emi = principal / months
        else:
            factor = Decimal(pow((1 + float(monthly_rate)), months))

            emi = (
                principal
                * monthly_rate
                * factor
            ) / (factor - Decimal("1"))

        total_payment = emi * months
        total_interest = total_payment - principal

        # Generate amortization schedule
        schedule = AmortizationService.generate(
            principal=principal,
            annual_rate=annual_rate,
            emi=emi,
            months=months,
        )

        # Ensure JSON serializable values
        cleaned_schedule = []

        for row in schedule:
            cleaned_schedule.append({
                "month": int(row["month"]),
                "emi": float(row["emi"]),
                "principal": float(row["principal"]),
                "interest": float(row["interest"]),
                "balance": float(row["balance"]),
            })

        return {
            "monthly_emi": float(round(emi, 2)),
            "total_payment": float(round(total_payment, 2)),
            "total_interest": float(round(total_interest, 2)),
            "months": int(months),
            "schedule": cleaned_schedule,
        }