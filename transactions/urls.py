from django.urls import path
from transactions import views

urlpatterns = [
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw"),
]
