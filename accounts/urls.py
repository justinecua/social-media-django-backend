from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    GetAllAccounts,
    Login,
    Register,
    ForgotPassword,
    )

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('getAllAccounts/', GetAllAccounts.as_view(), name='getAllAccounts'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'), 
    path('forgotPassword/', ForgotPassword.as_view(), name='forgotPassword'), 
]

