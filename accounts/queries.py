import logging
import secrets
import hashlib
from django.db import connections
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import socket
import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN")

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def getAllAccounts():
    try:
        query = f"""
            SELECT * FROM glow.glow.accounts_account;
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

def login(username, password):
    try:
        connection = connections['default']
        cursor = connection.cursor()

        query = """
                SELECT 
                    aa.firstname, 
                    aa.lastname, 
                    aa.gender, 
                    aa.bio, 
                    aa.age, 
                    aa.birthday, 
                    aa.profile_photo, 
                    aa.cover_photo, 
                    aa.cover_photo_id_imagekit, 
                    aa.profile_photo_id_imagekit, 
                    au.username, 
                    au.password, 
                    au.date_joined, 
                    aa.id AS account_id, 
                    au.id AS user_id
                FROM glow.glow.accounts_account aa
                INNER JOIN glow.glow.auth_user au
                    ON aa.auth_user_id = au.id
                WHERE au.username = %s;

        """
        cursor.execute(query, (username,))
        user_row = cursor.fetchone()

        if not user_row:
            return {"error": "username_not_found"}

        columns = [desc[0] for desc in cursor.description]
        user_data = dict(zip(columns, user_row))

        hashed_password = user_data["password"]
        if not check_password(password, hashed_password):
            return {"error": "password_incorrect"}

        return user_data

    except Exception as error:
        print(f"Error: {error}")
        return {"error": "internal_error"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def register(username, email, password):
    connection = connections['default']
    cursor = connection.cursor()

    try:
        query_check_username = "SELECT id FROM glow.glow.auth_user WHERE username = %s"
        cursor.execute(query_check_username, (username,))
        if cursor.fetchone():
            return {"message": "Username is already taken.", "status": 400}

        query_check_email = "SELECT id FROM glow.glow.auth_user WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        if cursor.fetchone():
            return {"message": "Email is already in use.", "status": 400}

        hashed_password = make_password(password)
        date_joined = timezone.now()
        not_admin = "false"
        empty = ''
        is_active = 'true'

        query_insert_user = """
            INSERT INTO glow.glow.auth_user (username, email, password, date_joined, is_superuser, first_name, last_name, is_staff, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        cursor.execute(query_insert_user, (username, email, hashed_password, date_joined, not_admin, empty, empty, not_admin, is_active))
        user_id = cursor.fetchone()

        query_insert_account = """
            INSERT INTO glow.glow.accounts_account (auth_user_id)
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


def send_mail_via_mailgun(subject, message, recipient):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Glow <support@{MAILGUN_DOMAIN}>",
            "to": [recipient],
            "subject": subject,
            "text": message,
        },
    )


def forgot_password(email):
    connection = connections['default']
    cursor = connection.cursor()

    try:
        query_check_email = "SELECT id, username FROM glow.glow.auth_user WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        user = cursor.fetchone()

        if not user:
            return {"message": "Email not found.", "status": 404}

        user_id, username = user

        raw_token = secrets.token_urlsafe(32)  
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()  
        expires_at = timezone.now() + timezone.timedelta(hours=1)  

        query_insert_token = """
            INSERT INTO glow.glow.accounts_passwordreset (user_id, token, expires_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET token = EXCLUDED.token, expires_at = EXCLUDED.expires_at
        """
        cursor.execute(query_insert_token, (user_id, hashed_token, expires_at))
        connection.commit()

        local_ip = get_local_ip()
        reset_link = f"http://{FRONTEND_DOMAIN}/resetpassword?token={raw_token}"

        response = send_mail_via_mailgun(
            subject="Password Reset Request",
            message=f"""
            Hi {username},
            You recently requested a password reset. Click the link below to reset your password:
            {reset_link}
            If you did not request this change, please ignore this message. 
            This link will expire in 1 hour.
            """,
            recipient=email,
        )

        if response.status_code != 200:
            print("Mailgun API error:", response.text)
            return {"message": "Failed to send email.", "status": 500}

        print("From:", settings.DEFAULT_FROM_EMAIL)
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

def reset_password(token, new_password):
    connection = connections['default']
    cursor = connection.cursor()

    try:
        # Step 1: Hash the token
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        # Step 2: Find token record
        query_select = """
            SELECT user_id, expires_at
            FROM glow.glow.accounts_passwordreset
            WHERE token = %s
        """
        cursor.execute(query_select, (hashed_token,))
        token_record = cursor.fetchone()

        if not token_record:
            return {"message": "Invalid or expired token.", "status": 400}

        user_id, expires_at = token_record

        # Step 3: Check expiration
        if timezone.now() > expires_at:
            return {"message": "Token has expired.", "status": 400}

        # Step 4: Hash the new password and update user table
        hashed_password = make_password(new_password)
        query_update_password = """
            UPDATE glow.glow.auth_user
            SET password = %s
            WHERE id = %s
        """
        cursor.execute(query_update_password, (hashed_password, user_id))

        # Step 5: Invalidate/delete the reset token
        query_delete_token = """
            DELETE FROM glow.glow.accounts_passwordreset
            WHERE user_id = %s
        """
        cursor.execute(query_delete_token, (user_id,))

        # Step 6: Commit all changes
        connection.commit()

        return {"message": "Password has been reset successfully.", "status": 200}

    except Exception as e:
        connection.rollback()
        print("Error in reset_password:", e)
        return {"message": "An error occurred while resetting password.", "status": 500}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def getNewUsers():
    try:
        query = f"""
                SELECT profile_photo, username, date_joined, glow.glow.accounts_account.id FROM glow.glow.accounts_account
                LEFT JOIN glow.glow.auth_user ON glow.glow.accounts_account.auth_user_id = glow.glow.auth_user.id
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

def getProfile(profile_id):
    try:
        query = f"""
                SELECT * FROM glow.accounts_account
                LEFT JOIN glow.auth_user ON glow.accounts_account.auth_user_id = glow.auth_user.id
                WHERE glow.accounts_account.id = %s
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (profile_id,))

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

def getTotalGlowsPostByUser(account_id):
    try:
        query = f"""
            SELECT COUNT(*) FROM glow.interactions_glow
            LEFT JOIN glow.posts_post ON post_id = glow.posts_post.id
            WHERE glow.posts_post.account_id =  %s 
            """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result[0] if result else 0 

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()
