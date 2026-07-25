from decimal import Decimal
from math import pow


class PrepaymentService:

    @staticmethod
    def calculate(
        principal,
        annual_rate,
        tenure,
        prepayment,
    ):

        principal = Decimal(principal)
        annual_rate = Decimal(annual_rate)
        prepayment = Decimal(prepayment)

        monthly_rate = annual_rate / Decimal("1200")

        factor = Decimal(
            pow(1 + float(monthly_rate), tenure)
        )

        emi = (
            principal
            * monthly_rate
            * factor
        ) / (factor - 1)

        new_principal = principal - prepayment

        if new_principal < 0:
            new_principal = Decimal("0")

        factor2 = Decimal(
            pow(1 + float(monthly_rate), tenure)
        )

        new_emi = (
            new_principal
            * monthly_rate
            * factor2
        ) / (factor2 - 1)

        total_interest_before = (emi * tenure) - principal

        total_interest_after = (
            new_emi * tenure
        ) - new_principal

        saved = (
            total_interest_before
            - total_interest_after
        )

        return {

            "old_emi": round(float(emi), 2),

            "new_emi": round(float(new_emi), 2),

            "interest_saved": round(float(saved), 2),

            "new_principal": round(float(new_principal), 2),
        }