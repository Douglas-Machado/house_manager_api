from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from ..models import Profile, House


class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = AuthUser

    email = serializers.EmailField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
    
        fields = '__all__'

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'first_name', 'last_name')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        depth = 2
        fields = ('id', 'birth_date', 'house_id', 'house_admin', 'user')
    user = AuthUserSerializer()

class HouseSerializer(serializers.Serializer):
    class Meta:
        model = House

    id = serializers.IntegerField()
    name = serializers.CharField()
    total_bills = serializers.DecimalField(max_digits=7, decimal_places=2)
