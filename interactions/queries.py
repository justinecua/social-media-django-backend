import logging
from django.db import connections
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from posts.queries import time_ago
from datetime import datetime
import pytz

def countGlows(post_id):
    try:
        query = f"""
                SELECT COUNT(*)
                FROM glow.interactions_glow
                WHERE glow.interactions_glow.post_id = %s
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (post_id,))

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]

        return results

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def getProfileGlows(post_id):
    try:
        query = f"""
                SELECT glow.interactions_glow.id AS glow_id, timestamp, account_id, post_id, firstname, lastname, profile_photo
                FROM glow.interactions_glow
                JOIN glow.accounts_account ON glow.interactions_glow.account_id = glow.accounts_account.id
                WHERE glow.interactions_glow.post_id = %s
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (post_id,))

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]

        return results

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def countComments(post_id):
    try:
        query = f"""
                SELECT COUNT(*) AS total_comments
                FROM glow.interactions_comment
                WHERE glow.interactions_comment.post_id = %s
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (post_id,))

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]

        return results
        
    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def showComments(post_id):
    try:
        query = f"""
            SELECT 
                c.id AS comment_id,
                c.content AS comment,
                c."dateTime",
                u.username,
                a.profile_photo
            FROM glow.glow.interactions_comment AS c
            LEFT JOIN
                glow.glow.accounts_account AS a ON c.account_id = a.id
            LEFT JOIN
                glow.glow.auth_user AS u ON a.auth_user_id = u.id
            WHERE c.post_id = %s
            ORDER BY c."dateTime" ASC;
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (post_id,))

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]
        for comment in results:
            if "dateTime" in comment and isinstance(comment["dateTime"], datetime):
                comment["dateTime"] = time_ago(comment["dateTime"])

        return results

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def addComment(comment, postId, accID):
    connection = None
    cursor = None
    try:
        now = datetime.now(pytz.utc)

        connection = connections["default"]
        cursor = connection.cursor()

        glow_query = """
            INSERT INTO glow.glow.interactions_comment (content, "dateTime", post_id, account_id )
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(glow_query, (comment, now, postId, accID))

        connection.commit()
        return {"status": "success", "message": "Comment added successfully3"}

    except Exception as error:
        print(f"Error: {error}")
        if connection:
            connection.rollback()
        return {"status": "error", "message": "Something went wrong."}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
