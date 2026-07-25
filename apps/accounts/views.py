from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum

from apps.calculator.models import LoanCalculation
from .forms import ProfileUpdateForm


def login_view(request):
    """
    User Login
    """

    if request.user.is_authenticated:
        return redirect("home")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def register(request):
    """
    User Registration
    """

    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def logout_view(request):
    """
    User Logout
    """

    logout(request)

    return redirect("login")

@login_required
def profile(request):

    calculations = LoanCalculation.objects.filter(
        user=request.user
    )

    context = {
        "total_calculations": calculations.count(),

        "total_loan_amount":
            calculations.aggregate(
                Sum("loan_amount")
            )["loan_amount__sum"] or 0,

        "total_interest":
            calculations.aggregate(
                Sum("total_interest")
            )["total_interest__sum"] or 0,

        "average_emi":
            round(
                calculations.aggregate(
                    Avg("monthly_emi")
                )["monthly_emi__avg"] or 0,
                2,
            ),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required
def edit_profile(request):

    form = ProfileUpdateForm(
        request.POST or None,
        instance=request.user,
    )

    if request.method == "POST":

        if form.is_valid():
            form.save()

            return redirect("profile")

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )