from rest_framework import serializers
from ..models import Profile, House
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=24)
    first_name = serializers.CharField(min_length=2, max_length=64)
    last_name = serializers.CharField(min_length=2, max_length=64)

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_email(self, value):
        """
        Check if email already exists
        """
        if Profile.objects.filter(email=value):
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = Profile.objects.create(email=validated_data['email'],
                                      first_name=validated_data['first_name'],
                                      last_name=validated_data['last_name'],
                                      birth_date=validated_data['birth_date'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('created_at', 'updated_at', 'groups',
                   'user_permissions', 'last_login', 'is_superuser')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=24)
    name = serializers.CharField(min_length=2, max_length=64)

    class Meta:
        model = House
        fields = '__all__'

    def create(self, validated_data):
        house = House.objects.create(name=validated_data['name'])
        house.password = make_password(validated_data['password'])
        house.save()
        return house
