from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .managers import Manager


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ("current", "Current"),
        ("savings", "Savings"),
    )
    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = None 
    bvn = models.CharField(max_length=11)
    nin = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    account_number = models.CharField(max_length=10)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # when creating superuser
    
    objects = Manager()
    
    def __str__(self):
        return self.email
