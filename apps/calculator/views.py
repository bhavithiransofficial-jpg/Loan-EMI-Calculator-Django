from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .services.excel_export import ExcelExportService
from .comparison_forms import LoanComparisonForm
from .forms import LoanCalculatorForm
from .models import LoanCalculation
from .services.emi import EMICalculatorService
from .services.export import PDFExportService
from io import BytesIO
from .eligibility_forms import LoanEligibilityForm
from .services.eligibility import LoanEligibilityService
from .prepayment_forms import PrepaymentForm
from .services.prepayment import PrepaymentService

@login_required
def home(request):
    form = LoanCalculatorForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():

        result = EMICalculatorService.calculate(
            principal=form.cleaned_data["loan_amount"],
            annual_rate=form.cleaned_data["annual_interest_rate"],
            tenure=form.cleaned_data["loan_tenure"],
            tenure_type=form.cleaned_data["tenure_type"],
        )

        LoanCalculation.objects.create(
            user=request.user,
            loan_amount=form.cleaned_data["loan_amount"],
            annual_interest_rate=form.cleaned_data["annual_interest_rate"],
            loan_tenure=form.cleaned_data["loan_tenure"],
            tenure_type=form.cleaned_data["tenure_type"],
            monthly_emi=result["monthly_emi"],
            total_interest=result["total_interest"],
            total_payment=result["total_payment"],
            schedule=result["schedule"],  # Remove this if your model doesn't have this field yet
        )

    return render(
        request,
        "home.html",
        {
            "form": form,
            "result": result,
        },
    )


@login_required
def dashboard(request):

    calculations = LoanCalculation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    context = {
        "recent_calculations": calculations[:5],
        "total_calculations": calculations.count(),
        "total_loan_amount": calculations.aggregate(
            Sum("loan_amount")
        )["loan_amount__sum"] or 0,
        "total_interest": calculations.aggregate(
            Sum("total_interest")
        )["total_interest__sum"] or 0,
        "average_emi": round(
            calculations.aggregate(
                Avg("monthly_emi")
            )["monthly_emi__avg"] or 0,
            2,
        ),
        "loan_labels": [
            c.created_at.strftime("%d-%m")
            for c in calculations
        ],
        "loan_amounts": [
            float(c.loan_amount)
            for c in calculations
        ],
    }

    return render(
        request,
        "calculator/dashboard.html",
        context,
    )


@login_required
def history(request):

    calculations = LoanCalculation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    search = request.GET.get("search")

    if search:
        calculations = calculations.filter(
            Q(loan_amount__icontains=search)
        )

    paginator = Paginator(calculations, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "calculator/history.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@login_required
def calculation_detail(request, pk):

    calculation = get_object_or_404(
        LoanCalculation,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "calculator/detail.html",
        {
            "calculation": calculation,
        },
    )


@login_required
def delete_calculation(request, pk):

    calculation = get_object_or_404(
        LoanCalculation,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        calculation.delete()
        return redirect("history")

    return render(
        request,
        "calculator/delete.html",
        {
            "calculation": calculation,
        },
    )


@login_required
def export_pdf(request, pk):

    calculation = get_object_or_404(
        LoanCalculation,
        pk=pk,
        user=request.user,
    )

    pdf = PDFExportService.generate_report(calculation)

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="loan_report_{pk}.pdf"'

    return response


@login_required
def compare_loans(request):

    form = LoanComparisonForm(request.POST or None)

    comparison = None

    if request.method == "POST" and form.is_valid():

        loan_a = EMICalculatorService.calculate(
            principal=form.cleaned_data["loan_amount"],
            annual_rate=form.cleaned_data["interest_rate_1"],
            tenure=form.cleaned_data["tenure"],
            tenure_type="months",
        )

        loan_b = EMICalculatorService.calculate(
            principal=form.cleaned_data["loan_amount"],
            annual_rate=form.cleaned_data["interest_rate_2"],
            tenure=form.cleaned_data["tenure"],
            tenure_type="months",
        )

        comparison = {
            "loan_a": loan_a,
            "loan_b": loan_b,
        }

    return render(
        request,
        "calculator/compare.html",
        {
            "form": form,
            "comparison": comparison,
        },
    )


@login_required
def amortization_schedule(request, pk):

    calculation = get_object_or_404(
        LoanCalculation,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "calculator/amortization_schedule.html",
        {
            "calculation": calculation,
            "schedule": calculation.schedule,
        },
    )

@login_required
def export_excel(request):

    calculations = LoanCalculation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    workbook = ExcelExportService.generate(calculations)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    response["Content-Disposition"] = (
        'attachment; filename="loan_history.xlsx"'
    )

    return response

@login_required
def loan_eligibility(request):

    form = LoanEligibilityForm(
        request.POST or None
    )

    result = None

    if request.method == "POST" and form.is_valid():

        result = LoanEligibilityService.calculate(

            income=form.cleaned_data[
                "monthly_income"
            ],

            expenses=form.cleaned_data[
                "monthly_expenses"
            ],

            annual_rate=form.cleaned_data[
                "annual_interest_rate"
            ],

            months=form.cleaned_data[
                "tenure"
            ],

        )

    return render(

        request,

        "calculator/eligibility.html",

        {

            "form": form,

            "result": result,

        },

    )
@login_required
def prepayment(request):

    form = PrepaymentForm(request.POST or None)

    result = None

    if request.method == "POST" and form.is_valid():

        result = PrepaymentService.calculate(

            principal=form.cleaned_data["loan_amount"],

            annual_rate=form.cleaned_data["annual_interest_rate"],

            tenure=form.cleaned_data["tenure"],

            prepayment=form.cleaned_data["prepayment"],

        )

    return render(

        request,

        "calculator/prepayment.html",

        {

            "form": form,

            "result": result,

        },

    )