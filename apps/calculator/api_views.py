from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import LoanCalculation
from .serializers import LoanCalculationSerializer


class LoanHistoryAPI(generics.ListAPIView):
    serializer_class = LoanCalculationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoanCalculation.objects.filter(
            user=self.request.user
        ).order_by("-created_at")