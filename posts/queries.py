import logging
from django.db import connections
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime
import pytz


def time_ago(post_datetime):
    now = datetime.now(pytz.utc)
    time_diff = now - post_datetime

    if time_diff.total_seconds() < 60:
        return "• Just now"
    elif time_diff.total_seconds() < 3600:
        minutes = int(time_diff.total_seconds() / 60)
        return f"• {minutes} minute{'s' if minutes != 1 else ''} ago"
    elif time_diff.total_seconds() < 86400:
        hours = int(time_diff.total_seconds() / 3600)
        return f"• {hours} hour{'s' if hours != 1 else ''} ago"
    elif time_diff.total_seconds() < 604800:
        days = int(time_diff.total_seconds() / 86400)
        return f"• {days} day{'s' if days != 1 else ''} ago"
    elif time_diff.total_seconds() < 2592000:
        weeks = int(time_diff.total_seconds() / 604800)
        return f"• {weeks} week{'s' if weeks != 1 else ''} ago"
    elif time_diff.total_seconds() < 31536000:
        months = int(time_diff.total_seconds() / 2592000)
        return f"• {months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(time_diff.total_seconds() / 31536000)
        return f"• {years} year{'s' if years != 1 else ''} ago"


def getPosts(offset=0, limit=5):
    try:
        query = f"""
            SELECT 
                p.id,
                p.account_id,
                p.caption,
                p."dateTime",
                u.username,
                a.firstname,
                a.lastname,
                a.profile_photo,
                COUNT(DISTINCT glows.id) AS glow_count,
                COUNT(DISTINCT comments.id) AS comment_count,
                ARRAY_AGG(DISTINCT ph.link) AS photos
            FROM
                glow.public.posts_post AS p
            LEFT JOIN
                glow.public.accounts_account AS a ON p.account_id = a.id
            LEFT JOIN
                glow.public.auth_user AS u ON a.auth_user_id = u.id
            LEFT JOIN
                glow.public.posts_photo AS ph ON p.id = ph.post_id
            LEFT JOIN
                glow.public.interactions_glow AS glows ON p.id = glows.post_id
            LEFT JOIN
                glow.public.interactions_comment AS comments ON p.id = comments.post_id
            GROUP BY 
                p.id, p.account_id, p.caption, p."dateTime", u.username, a.firstname, a.lastname, a.profile_photo
            ORDER BY 
                p."dateTime" DESC
            OFFSET {offset} LIMIT {limit};
        """

        connection = connections["default"]
        cursor = connection.cursor()
        cursor.execute(query)

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]

        for post in results:
            if "dateTime" in post and isinstance(post["dateTime"], datetime):
                post["dateTime"] = time_ago(post["dateTime"])
            if "photos" in post and isinstance(post["photos"], list):
                post["photos"] = [
                    photo
                    for photo in post["photos"]
                    if photo and isinstance(photo, str) and photo.strip()
                ]

        return {'results': results}

    except Exception as error:
        print(f"Error: {error}")
        return {'results': []}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

