from django.contrib import admin
from transactions import models

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount", "status", "description")
    search_fields = ("sender", "receiver", "amount")

admin.site.register(models.Transactions, TransactionAdmin)

class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'principal_amount', 'is_approved', 'created_at')
    search_fields = ('user', 'principal_amount', 'is_approved')

admin.site.register(models.LoanApplications, LoanAdmin)