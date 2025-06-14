import logging
import secrets
from django.db import connections
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
import socket
import os
import requests

def getTotalFriends(account_id):
    try:
        query = f"""
            SELECT COUNT(*) AS total_friends
            FROM glow.friends_friend
            WHERE status = 'Friends' AND (user_id = %s OR friend_id = %s);
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (account_id, account_id))
        result = cursor.fetchone()
        return result[0] if result else 0 

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()
