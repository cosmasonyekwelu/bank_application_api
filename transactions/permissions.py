from rest_framework.permissions import BasePermission
from accounts.models import Accounts


class IscurrentAccount(BasePermission):
    message = "You do not have permission to perform this action."
    
    def has_permission(self, request, view):
        try:
         user_account = Accounts.objects.get(user=request.user.id)
        except Accounts.DoesNotExist:
            return False
        if request.method in ["POST"] and user_account.account_type == "current":
            return True
        else:
            return False
            