from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    GetAllAccounts,
    Login,
    Register,
    ForgotPassword,
    GetNewUsers,
    GetProfile,
    GetTotalGlowsPostByUser,
    Logout,
    ResetPassword,
    )

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('getAllAccounts/', GetAllAccounts.as_view(), name='getAllAccounts'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'), 
    path('forgotPassword/', ForgotPassword.as_view(), name='forgotPassword'), 
    path('resetPassword/', ResetPassword.as_view(), name='resetPassword'), 
    path('getNewUsers/', GetNewUsers.as_view(), name='getNewUsers'),
    path('profile/<int:profile_id>/', GetProfile.as_view(), name='getProfile'),
    path('getTotalGlowsByUser/<int:profile_id>/', GetTotalGlowsPostByUser.as_view(), name='getTotalGlowsByUser'),
]

