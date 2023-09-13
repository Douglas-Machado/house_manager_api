from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

AuthUser._meta.get_field('email')._unique = True

class House(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    total_bills = models.DecimalField(decimal_places=2, max_digits=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    house = models.ForeignKey(House, null=True, on_delete=models.CASCADE)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    house_admin = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=AuthUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
