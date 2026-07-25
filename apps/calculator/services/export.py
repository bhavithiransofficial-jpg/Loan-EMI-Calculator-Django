from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


class PDFExportService:

    @staticmethod
    def generate_report(calculation):

        buffer = BytesIO()

        document = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>Loan EMI Report</b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        data = [

            ["Loan Amount", f"₹ {calculation.loan_amount}"],

            ["Interest Rate", f"{calculation.annual_interest_rate}%"],

            ["Tenure", f"{calculation.loan_tenure} {calculation.tenure_type}"],

            ["Monthly EMI", f"₹ {calculation.monthly_emi}"],

            ["Total Interest", f"₹ {calculation.total_interest}"],

            ["Total Payment", f"₹ {calculation.total_payment}"],

        ]

        table = Table(data)

        table.setStyle(

            TableStyle(

                [

                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),

                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

                ]

            )

        )

        elements.append(table)

        document.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf