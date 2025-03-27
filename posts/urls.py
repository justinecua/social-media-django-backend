from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    GetPosts,

    )

urlpatterns = [
    path('getPosts/', GetPosts.as_view(), name='getPosts'), 
]

