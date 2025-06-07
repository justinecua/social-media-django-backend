from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from posts.services.external_feeds import (
    getJokes,
    getUselessFacts,
    getAdvice,
    getQuotes,
    getRiddle,
    getMemeFromReddit,
    getRandomAnimeImage,

)

from .queries import (
    getPosts,
    getPostsByUser
)

from .api.decorators import (
    get_posts_decorator,
)


class GetPosts(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 5))
        data = getPosts(offset, limit)
        return Response(data)

class GetPostsByUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, account_id):
        data = getPostsByUser(account_id)
        return Response(data)

# External Api
class GetJokes(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getJokes()
        return Response(data)


class GetUselessFacts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getUselessFacts()
        return Response(data)


class GetAdvice(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getAdvice()
        return Response(data)


class GetQuotes(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getQuotes()
        return Response(data)


class GetRiddles(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getRiddle()
        return Response(data)


class GetMemeFromReddit(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getMemeFromReddit()
        return Response(data)


class GetRandomAnimeImage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = getRandomAnimeImage()
        return Response(data)
