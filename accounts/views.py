
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from datetime import timedelta



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

        user_data.pop("password", None)
                      
        refresh = RefreshToken()
        refresh.payload.update({"user_id": user_data["user_id"], "username": user_data["username"]})

        #Websocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global",
            {
                "type": "user_logged_in",
                "username": username,
            }
        )

        refresh["user_id"] = user_data["user_id"]
        refresh["username"] = user_data["username"]

        response = JsonResponse({"user": user_data})
        print(response)

        access_token_expiry = timedelta(minutes=5)
        refresh_token_expiry = timedelta(days=7)

        # TEMPORARY DEV-ONLY: set `secure=False`
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,            # 🔥 change this for development
            samesite="Lax",          # change back from "None" since not cross-site now
            max_age=int(access_token_expiry.total_seconds())
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=int(refresh_token_expiry.total_seconds())
        )


        return response

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

from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  

        return Response({
            "user": {
                "username": user.username,
                "id": user.id,
                "email": user.email,
                "date_joined": user.date_joined,
            }
        })

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")  
        if not refresh_token:
            raise AuthenticationFailed("Refresh token not found in cookies.")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token})
        except Exception:
            raise AuthenticationFailed("Invalid refresh token.")
