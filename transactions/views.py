from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from accounts.models import Accounts
from django.db import transaction
from transactions import serializers


def deposit_money(user, incoming_amount):
    with transaction.atomic():
        user.amount += float(incoming_amount)
        user.save()
        return True


def transfer_money(sender, receiver, amount):
    with transaction.atomic():
        sender.amount -= float(amount)
        sender.save()

        receiver.amount += float(amount)
        receiver.save()
        return True


@api_view(["POST"])
def deposit(request):
    try:
        account = Accounts.objects.get(user=request.user.id)
    except Accounts.DoesNotExist:
        return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
    deposit = deposit_money(
        user=account, incoming_amount=request.data.get("amount"))

    if deposit:
        transaction_info = {
            "sender": account.id,
            "receiver": account.id,
            "amount": account.amount,
            "status": "success",
            "description": "transfer to self"
        }

        serializer = serializers.TransactionSerializer(data=transaction_info)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Deposit successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Deposit failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def transfer(request):
    try:
        sender = Accounts.objects.get(user=request.user.id)

    except Accounts.DoesNotExist:
        return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        receiver = Accounts.objects.get(
            account_number=request.data.get("account_number"))
    except Accounts.DoesNotExist:
        return Response({"message": "Receiver account not found"}, status=status.HTTP_404_NOT_FOUND)

    transfer = transfer_money(
        sender=sender, receiver=receiver, amount=request.data.get("amount"))

    if transfer:
        transaction_info = {
            "sender": sender.id,
            "receiver": receiver.id,
            "amount": receiver.amount,
            "status": "success",
            "description": f"transfer to {receiver.account_number}"
        }

        serializer = serializers.TransactionSerializer(data=transaction_info)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Transfer successful to {receiver.account_number}"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
