from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, HouseViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet)
router.register(r'users', UserViewSet)
router.register(r'houses', HouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
