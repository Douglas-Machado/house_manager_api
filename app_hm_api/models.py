from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

User._meta.get_field("email")._unique = True


class House(models.Model):
    name = models.TextField(max_length=255)
    total_bills = models.DecimalField(decimal_places=2, null=True, max_digits=7)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    email = models.EmailField(_("email address"), unique=True)
    house = models.ForeignKey(House, null=True, on_delete=models.SET_NULL)
    owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def login(self, password: str):
        if not check_password(password, self.password):
            raise ValidationError("test")
        return password


# class Stock(models.Model):
#     id = models.AutoField(primary_key=True)
#     house_id = models.ForeignKey(House, on_delete=models.CASCADE)
#     name = models.TextField(max_length=256, null=False)
#     category = models.TextField(max_length=256, null=True)
#     quantity = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class StockLog(models.Model):
#     id = models.AutoField(primary_key=True)
#     stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
