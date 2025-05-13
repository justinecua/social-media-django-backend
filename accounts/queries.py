import logging
import secrets
import hashlib
from django.db import connections
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import socket

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def getAllAccounts():
    try:
        query = f"""
            SELECT * FROM public.accounts_account;
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


from django.contrib.auth.hashers import check_password

def login(username, password):
    try:
        connection = connections['default']
        cursor = connection.cursor()

        # Fetch the user by username
        query = """
            SELECT firstname, lastname, gender, bio, age, birthday, profile_photo, cover_photo, 
                   cover_photo_id_imagekit, profile_photo_id_imagekit, username, password, date_joined, 
                   public.auth_user.id
            FROM public.accounts_account
            INNER JOIN public.auth_user
            ON public.accounts_account.auth_user_id = public.auth_user.id
            WHERE username = %s
        """
        cursor.execute(query, (username,))
        user_row = cursor.fetchone()

        if not user_row:
            return None

        columns = [desc[0] for desc in cursor.description]
        user_data = dict(zip(columns, user_row))

        hashed_password = user_data["password"]
        if not check_password(password, hashed_password):
            return None

        return user_data

    except Exception as error:
        print(f"Error: {error}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def register(username, email, password):
    connection = connections['default']
    cursor = connection.cursor()

    try:
        query_check_username = "SELECT id FROM public.auth_user WHERE username = %s"
        cursor.execute(query_check_username, (username,))
        if cursor.fetchone():
            return {"message": "Username is already taken.", "status": 400}

        query_check_email = "SELECT id FROM public.auth_user WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        if cursor.fetchone():
            return {"message": "Email is already in use.", "status": 400}

        hashed_password = make_password(password)
        date_joined = timezone.now()
        not_admin = "false"
        empty = ''
        is_active = 'true'

        query_insert_user = """
            INSERT INTO public.auth_user (username, email, password, date_joined, is_superuser, first_name, last_name, is_staff, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        cursor.execute(query_insert_user, (username, email, hashed_password, date_joined, not_admin, empty, empty, not_admin, is_active))
        user_id = cursor.fetchone()

        query_insert_account = """
            INSERT INTO public.accounts_account (auth_user_id)
            VALUES (%s)
        """
        cursor.execute(query_insert_account, (user_id,))

        connection.commit()  
        return {"message": "Signup successful!", "status": 201}

    except Exception as error:
        connection.rollback()
        print(f"Error: {error}")
        return {"message": "An error occurred.", "status": 500}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def forgot_password(email):
    connection = connections['default']
    cursor = connection.cursor()

    try:
        query_check_email = "SELECT id, username FROM public.auth_user WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        user = cursor.fetchone()

        if not user:
            return {"message": "Email not found.", "status": 404}

        user_id, username = user

        raw_token = secrets.token_urlsafe(32)  # Raw token for email link
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()  # Securely store the hashed token
        expires_at = timezone.now() + timezone.timedelta(hours=1)  # Token expires in 1 hour

        query_insert_token = """
            INSERT INTO public.password_reset (user_id, token, expires_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET token = EXCLUDED.token, expires_at = EXCLUDED.expires_at
        """
        cursor.execute(query_insert_token, (user_id, hashed_token, expires_at))
        connection.commit()

        local_ip = get_local_ip()
        reset_link = f"http://{local_ip}:8000/reset-password?token={raw_token}"

        send_mail(
            subject="Password Reset Request",
            message=f"""
            Hi {username},
            
            You recently requested a password reset. Click the link below to reset your password:
            
            {reset_link}
            
            If you did not request this change, please ignore this message.
            
            This link will expire in 1 hour.
            """,
            from_email=settings.DEFAULT_FROM_EMAIL, 
            recipient_list=[email],
            fail_silently=False,
        )

        return {"message": "Password reset email sent.", "status": 200}

    except Exception as error:
        connection.rollback()
        print(f"Error: {error}")
        return {"message": "An error occurred.", "status": 500}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def getNewUsers():
    try:
        query = f"""
                SELECT profile_photo, username, date_joined FROM glow.public.accounts_account
                LEFT JOIN glow.public.auth_user ON glow.public.accounts_account.auth_user_id = glow.public.auth_user.id
                ORDER BY date_joined DESC LIMIT 30
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
