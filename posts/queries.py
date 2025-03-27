import logging
from django.db import connections
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def getPosts():
    try:
        query = f"""
            SELECT 
                p.id,
                p.account_id,
                p.caption,
                p."dateTime",
                ARRAY_AGG(ph.link) AS photos
            FROM
                glow.posts_post AS p
            LEFT JOIN
                glow.accounts_account AS a ON p.account_id = a.id
            LEFT JOIN
                glow.auth_user AS u ON a.auth_user_id = u.id
            LEFT JOIN
                glow.posts_photo AS ph ON p.id = ph.post_id
            GROUP BY p.id, p.account_id, p.caption, p."dateTime";
                """

        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query)

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
