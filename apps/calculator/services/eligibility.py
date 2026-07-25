from decimal import Decimal
from math import pow


class LoanEligibilityService:

    @staticmethod
    def calculate(
        income,
        expenses,
        annual_rate,
        months,
    ):

        income = Decimal(income)
        expenses = Decimal(expenses)
        annual_rate = Decimal(annual_rate)

        disposable_income = income - expenses

        max_emi = disposable_income * Decimal("0.50")

        monthly_rate = annual_rate / Decimal("1200")

        if monthly_rate == 0:
            eligible_amount = max_emi * months

        else:

            factor = Decimal(
                pow(
                    (1 + float(monthly_rate)),
                    months,
                )
            )

            eligible_amount = (
                max_emi
                * (factor - 1)
            ) / (
                monthly_rate * factor
            )

        return {

            "income": round(income, 2),

            "expenses": round(expenses, 2),

            "disposable_income": round(
                disposable_income,
                2,
            ),

            "eligible_emi": round(
                max_emi,
                2,
            ),

            "eligible_amount": round(
                eligible_amount,
                2,
            ),

        }