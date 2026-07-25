from .models import LoanCalculation


def get_recent_calculations(limit=10):
    return LoanCalculation.objects.all()[:limit]