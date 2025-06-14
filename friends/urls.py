from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    GetTotalFriends
    )

urlpatterns = [
    path('getTotalFriends/<int:account_id>/', GetTotalFriends.as_view(), name='getTotalFriends'),
]

