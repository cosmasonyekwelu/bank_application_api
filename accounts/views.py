from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from accounts import serializers
from users.models import User

# Create your views here.


@api_view(["POST"])
def create_account(request):
    user = request.user.id
    account_data = request.data.copy()
    account_data['user'] = user

    serializer = serializers.CreateAccount(data=account_data)
    if serializer.is_valid():
        serializer.save(user=request.user)

        return Response({"message": "Your account has been created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_account(request):
    user_id = request.user.id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
