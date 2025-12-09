from rest_framework import serializers
from .models import Transactions



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['sender', 'receiver', 'amount', 'status']