from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet, UserViewSet, HouseViewSet

router = DefaultRouter()
router.register(r'auth', LoginViewSet)
router.register(r'users', UserViewSet)
router.register(r'houses', HouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
