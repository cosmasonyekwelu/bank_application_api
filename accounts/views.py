from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@api_view(["POST"])
def create_account(request):
    return Response({"message":"Your account has been created"},status=status.HTTP_201_CREATED)
