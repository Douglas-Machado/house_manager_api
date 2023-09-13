from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Profile, House


class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = User

    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = "__all__"


class HouseSerializer(serializers.Serializer):
    class Meta:
        model = House

    id = serializers.IntegerField()
    name = serializers.CharField()
    total_bills = serializers.DecimalField(max_digits=7, decimal_places=2)
