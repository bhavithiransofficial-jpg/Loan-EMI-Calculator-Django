from rest_framework import serializers
from .models import LoanCalculation


class LoanCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanCalculation
        fields = "__all__"