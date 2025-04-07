from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    GetPosts,
    GetJokes,
    GetUselessFacts,
    GetAdvice,
    GetQuotes,
    GetRiddles,
    GetMemeFromReddit,
    GetRandomAnimeImage,
)


urlpatterns = [
    path("getPosts/", GetPosts.as_view(), name="getPosts"),
    path("getJokes/", GetJokes.as_view(), name="getJokes"),
    path("getUselessFacts/", GetUselessFacts.as_view(), name="getUselessFacts"),
    path("getAdvice/", GetAdvice.as_view(), name="getAdvice"),
    path("getQuotes/", GetQuotes.as_view(), name="getQuotes"),
    path("getRiddles/", GetRiddles.as_view(), name="getRiddles"),
    path("getMemeFromReddit/", GetMemeFromReddit.as_view(), name="getMemeFromReddit"),
    path(
        "getRandomAnimeImage/",
        GetRandomAnimeImage.as_view(),
        name="getRandomAnimeImage",
    ),
]
