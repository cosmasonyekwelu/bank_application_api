from django.urls import path
from accounts import views

urlpatterns = [
    path("create/", views.create_account,name="create_account")
]
