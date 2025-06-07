
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .queries import (
    countGlows,
    getProfileGlows,
    countComments,
    showComments,
)

from .api.decorators import (
    count_glows_decorator,
    get_profile_glows_decorator,
    count_comments_decorator,
    show_comments_decorator
)


class CountGlows(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @count_glows_decorator()
    def get(self, request):
        post_id = request.data.get("post_id") 

        data = countGlows(post_id) 
        return Response(data)

class GetProfileGlows(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @get_profile_glows_decorator()
    def get(self, request):
        post_id = request.data.get("post_id") 

        data = getProfileGlows(post_id) 
        return Response(data)

class CountComments(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @count_comments_decorator()
    def get(self, request):
        post_id = request.data.get("post_id") 

        data = countComments(post_id) 
        return Response(data)

class ShowComments(APIView):
    permission_classes = (permissions.AllowAny,)

    @show_comments_decorator()
    def get(self, request, post_id):
        data = showComments(post_id)
        return Response(data)
