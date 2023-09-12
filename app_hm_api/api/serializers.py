from rest_framework.serializers import ModelSerializer, Serializer, CharField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()
