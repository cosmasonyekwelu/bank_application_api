from django.urls import path
from transactions import views

urlpatterns = [
    path('deposit/', views.deposit, name="deposit"),
    path('transfer/', views.transfer, name="transfer"),
    path('loan/', views.apply_for_loan, name="loan"),
]
