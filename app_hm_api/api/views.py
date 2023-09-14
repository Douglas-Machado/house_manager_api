from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import LoginSerializer, ProfileSerializer, HouseSerializer
from django.contrib.auth.models import User as AuthUser
from ..models import Profile, House
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction


class AuthViewSet(ModelViewSet):
    queryset = Profile.objects.all()

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
    )
    def register(self, request):
        user = None

        try:
            with transaction.atomic():
                user = AuthUser.objects.create_user(
                    username=request.data.get("username"),
                    email=request.data.get("email"),
                    password=request.data.get("password"),
                )
            if request.data.get("first_name"):
                user.first_name = request.data.get("first_name")
            if request.data.get("last_name"):
                user.last_name = request.data.get("last_name")
            if request.data.get("birth_date"):
                user.profile.birth_date = request.data.get("birth_date")
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)
            return Response({"error": ex.args[1]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        profile = Profile.objects.get(id=user.id)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": LoginSerializer(instance=profile).data
            },
            status=status.HTTP_200_OK
        )


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @action(detail=False, methods=["put"], url_path="add-house")
    def add_house(self, request):
        house_id = request.data.get("house_id")
        username = request.data.get("username")

        user = AuthUser.objects.get(username=username)

        user.profile.house_id = house_id
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]
