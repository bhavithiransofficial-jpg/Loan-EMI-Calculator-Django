from decimal import Decimal


class AmortizationService:

    @staticmethod
    def generate(principal, annual_rate, emi, months):
        """
        Generate month-by-month amortization schedule.
        """

        schedule = []

        balance = Decimal(principal)

        monthly_rate = Decimal(annual_rate) / Decimal("1200")

        for month in range(1, months + 1):

            interest = balance * monthly_rate

            principal_paid = emi - interest

            balance -= principal_paid

            if balance < 0:
                balance = Decimal("0")

            schedule.append({
                "month": month,
                "emi": float(round(emi, 2)),
                "principal": float(round(principal_paid, 2)),
                "interest": float(round(interest, 2)),
                "balance": float(round(balance, 2)),
            })

        return schedule