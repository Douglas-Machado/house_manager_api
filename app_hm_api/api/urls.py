from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({"get": "list"}), name="list_users"),
    # path('users/register', register_user),
]
