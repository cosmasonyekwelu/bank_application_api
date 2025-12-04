from rest_framework.serializers import ModelSerializer
from .models import Accounts

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"
