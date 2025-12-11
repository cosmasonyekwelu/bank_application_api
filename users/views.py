from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User
from users import serializers

from drf_spectacular.utils import extend_schema, OpenApiExample

# Authentication Imports
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

# Create your views here.


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=['POST'],
    request=dict,
    responses={
        200:{"message":"Login Successful"},
        400:{"message":"Login Failed"},
    },
    examples=[
        OpenApiExample(
            "Login",
            value={
                "email":"email@gmail.com",
                "password":"your pass"
            }
        )
    ],
    summary="Login User",
    description="this is for login"
)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def login(request):
    incoming_email = request.data.get("email")
    incoming_password = request.data.get("password")
    user = authenticate(email=incoming_email, password=incoming_password)
    if user is not None:
        access_token = AccessToken.for_user(user=user)
        refresh_token = RefreshToken.for_user(user=user)
        return Response({
            "message": "User Login successful",
            "access": str(access_token),
            "refresh": str(refresh_token)
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(["PATCH"])
def update_user_details(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.UserSerializer(user, data=request.data , partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User details updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)