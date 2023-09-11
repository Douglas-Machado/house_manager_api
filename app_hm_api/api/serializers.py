from rest_framework.serializers import ModelSerializer
from ..models import House, User


class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'total_bills')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'age', 'house_id', 'admin')
