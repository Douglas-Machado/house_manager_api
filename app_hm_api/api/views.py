from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models import House, User
from .serializers import HouseSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

# @api_view(["GET"])
# def get_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
