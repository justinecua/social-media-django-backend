from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .queries import (
    getTotalFriends
)

class GetTotalFriends(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, account_id):
        data = getTotalFriends(account_id) 
        return Response(data)
