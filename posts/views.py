
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .queries import (
    getPosts,
)

from .api.decorators import (
    get_posts_decorator,
)

class GetPosts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @get_posts_decorator()
    def get(self, request):
        data = getPosts() 
        return Response(data)


