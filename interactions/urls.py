from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CountGlows,
    GetProfileGlows,
    CountComments,
    ShowComments,
    )

urlpatterns = [
    path('countGlows/', CountGlows.as_view(), name='countGlows'),
    path('getProfileGlows/', GetProfileGlows.as_view(), name='getProfileGlows'),
    path('countComments/', CountComments.as_view(), name='countComments'),
    path('showComments/', ShowComments.as_view(), name='showComments')
]

