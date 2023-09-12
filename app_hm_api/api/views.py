from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.contrib.auth.models import User

class LoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Check the action being performed and return the appropriate permissions
        if self.action in ('register', 'login'):
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path="register")
    def register(self, request):
        user = User.objects.create_user(
            username = request.data.get("username"),
            email=request.data.get("email"),
            password=request.data.get("password")
        )
        if request.data.get("first_name"):
            user.first_name = request.data.get("first_name")
        if request.data.get("last_name"):
            user.last_name = request.data.get("last_name")
        user.save()
        return Response(UserSerializer(instance=user).data)
