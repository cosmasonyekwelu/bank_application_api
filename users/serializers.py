from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(required=False)
    account_type = serializers.CharField(required=False)
    bvn = serializers.CharField(required=False)
    nin = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        password = attrs.get("password")
        validate_password(password=password)
        return attrs

    def create(self, validated_attrs):
        user = User(
            first_name=validated_attrs.get("first_name"),
            last_name=validated_attrs.get("last_name"),
            email=validated_attrs.get("email"),
            phone_number=validated_attrs.get("phone_number"),
        )
        user.set_password(validated_attrs.get("password"))
        user.save()
        return user
