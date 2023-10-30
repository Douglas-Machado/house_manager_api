from rest_framework import serializers
from ..models import Profile, House


class RegisterSerializer(serializers.ModelSerializer):

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
    class Meta:
        model = House
