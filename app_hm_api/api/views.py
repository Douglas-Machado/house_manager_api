from . import serializers
from ..models import Profile, House
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class AuthViewSet(ModelViewSet):
    queryset = Profile.objects.all()

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
    )
    def register(self, request):
        data = request.data

        try:
            serializer = serializers.RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        email = request.data.get("email")
        try:
            profile = Profile.objects.get(email=email)
            profile.login(request.data.get("password"))

            refresh = RefreshToken.for_user(profile)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "profile": serializers.LoginSerializer(instance=profile).data
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        profile_id = data.pop('profile_id')

        # try:
        profile = get_object_or_404(Profile, id=profile_id)
        
        if profile.house:
            return Response({"error": "User already own a house"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.HouseSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        profile.house_id = serializer.data.get('id')
        profile.owner = True
        profile.save()
        return Response(status=status.HTTP_201_CREATED)
        # except Exception:


        return Response(status=status.HTTP_204_NO_CONTENT)
