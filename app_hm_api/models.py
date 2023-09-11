from django.db import models
from django.contrib.auth.hashers import make_password
from os import getenv

# Create your models here.
class House(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=256)
    total_bills = models.DecimalField(decimal_places=2, max_digits=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.TextField(max_length=256)
    email = models.EmailField(max_length=256, null=False, unique=True)
    password = models.TextField()
    age = models.IntegerField()
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.s_password = make_password(self.s_password)
        super(User, self).save(*args, **kwargs)

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.TextField(max_length=256, null=False)
    category = models.TextField(max_length=256, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockLog(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
