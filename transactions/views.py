from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

@api_view(["POST"])
def deposit(request):
        return Response({"message": "Deposit successful"}, status=status.HTTP_200_OK)
    
    
    
    
@api_view(["POST"])
def withdraw(request):
    return Response({"message": "Withdraw successful"}, status=status.HTTP_200_OK)