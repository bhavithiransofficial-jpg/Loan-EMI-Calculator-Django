from decimal import Decimal, ROUND_HALF_UP


class EMICalculatorService:

    @staticmethod
    def calculate(principal, annual_rate, tenure, tenure_type):

        principal = Decimal(principal)
        annual_rate = Decimal(annual_rate)

        months = tenure * 12 if tenure_type == "years" else tenure

        monthly_rate = annual_rate / Decimal("1200")

        if monthly_rate == 0:
            emi = principal / months
        else:
            factor = (Decimal("1") + monthly_rate) ** months

            emi = (
                principal
                * monthly_rate
                * factor
            ) / (factor - Decimal("1"))

        emi = emi.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        balance = principal

        schedule = []

        total_interest = Decimal("0.00")

        for month in range(1, months + 1):

            interest = (
                balance * monthly_rate
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            principal_paid = (
                emi - interest
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            balance = (
                balance - principal_paid
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            if balance < 0:
                balance = Decimal("0.00")

            total_interest += interest

            schedule.append(
                {
                    "month": month,
                    "emi": emi,
                    "interest": interest,
                    "principal": principal_paid,
                    "balance": balance,
                }
            )

        total_payment = emi * months

        return {
            "monthly_emi": emi,
            "total_interest": total_interest,
            "total_payment": total_payment,
            "months": months,
            "schedule": schedule,
        }