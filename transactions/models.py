from django.db import models


# Create your models here. using a self referential model relationship
class Transactions(models.Model):
    sender = models.ForeignKey(
        'accounts.Accounts', on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(
        'accounts.Accounts', on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver}"


class LoanApplications(models.Model):
    user = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE,
                             related_name='user_loan', null=True, blank=True)
    principal_amount = models.FloatField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
