from django.db import models

class Accounts(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ("current", "Current"),
        ("savings", "Savings"),
    )

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_account",
        null=True,
        blank=True
    )
    bvn = models.CharField(max_length=11)
    nin = models.CharField(max_length=11)
    account_number = models.CharField(max_length=10, null=True, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account: {self.account_number}"
