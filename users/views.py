from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(["POST"])
def register(request):
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
