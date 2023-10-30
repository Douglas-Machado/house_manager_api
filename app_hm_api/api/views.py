from . import serializers
from ..models import Profile, House
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken


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

    # @action(detail=False, methods=["put"], url_path="add-house")
    # def add_house(self, request):
    #     house_id = request.data.get("house_id")
    #     username = request.data.get("username")

    #     user.profile.house_id = house_id
    #     user.save()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
    permission_classes = [IsAuthenticated]
