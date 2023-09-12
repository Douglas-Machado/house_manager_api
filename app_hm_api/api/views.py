from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginViewSet(ModelViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=['post'], url_path="register", permission_classes=[AllowAny])
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

    @action(detail=False, methods=['post'], url_path="login", permission_classes=[AllowAny])
    def login(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                user = authenticate(username=username, password=password)

                if user is None:
                    return Response({
                        "message": "Invalid username or password"
                    }, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
        except Exception as ex:
            print(ex)
