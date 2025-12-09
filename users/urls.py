from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('update/', views.update_user_details, name="update_user_details"),
]
