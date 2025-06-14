
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .queries import (
    getAllAccounts,
    login,
    register,
    forgot_password,
    getNewUsers,
    getProfile,
    getTotalGlowsPostByUser,
    reset_password
)

from .api.decorators import (
    get_all_accounts_decorator,
    login_decorator,
    register_decorator,
    forgot_password_decorator
)

class GetAllAccounts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @get_all_accounts_decorator()
    def get(self, request):
        data = getAllAccounts() 
        return Response(data)

class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_data = login(username, password)

        if user_data is None or user_data.get("error") == "internal_error":
            return Response({"detail": "An error occurred."}, status=500)

        if user_data.get("error") == "username_not_found":
            return Response({"detail": "Username not found."}, status=404)

        if user_data.get("error") == "password_incorrect":
            return Response({"detail": "Password is incorrect."}, status=401)

        refresh = RefreshToken()
        refresh.payload.update({"user_id": user_data["user_id"], "username": user_data["username"]})

        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({"user": user_data, "tokens": tokens}, status=200)

class Logout(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    @register_decorator()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        data = register(username, email, password) 
        return Response(data)

class ForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)

    @forgot_password_decorator()
    def post(self, request):
        email = request.data.get("email")

        data = forgot_password(email) 
        return Response(data)

class ResetPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        data = reset_password(token, new_password)
        return Response(data)
    
class GetNewUsers(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        data = getNewUsers() 
        return Response(data)

class GetProfile(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, profile_id):
        data = getProfile(profile_id)
        return Response(data)

class GetTotalGlowsPostByUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, profile_id):
        data = getTotalGlowsPostByUser(profile_id)
        return Response(data)

