from rest_framework import serializers
from transactions import models


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transactions
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoanApplications
        fields = "__all__"
