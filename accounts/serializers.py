from rest_framework import serializers
from .models import Accounts
import random


class CreateAccount(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"
        # read_only_fields = ('user',)

    def validate(self, incoming_data):

        if len(incoming_data["bvn"]) != 11:
            raise serializers.ValidationError("BVN must be 11 digits")

        if len(incoming_data["nin"]) != 11:
            raise serializers.ValidationError("NIN must be 11 digits")

        return incoming_data

    def create(self, validated_data, **kwargs):
        account_number = ''.join([str(random.randint(0, 9))
                                 for _ in range(10)])

        account = Accounts(user=validated_data["user"],
                           bvn=validated_data.get("bvn"),
                           nin=validated_data.get("nin"),
                           account_type=validated_data.get("account_type"),
                           account_number=account_number)

        account.save()
        return account


class AccountDetails(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['user', 'account_number', 'account_type', 'amount']
