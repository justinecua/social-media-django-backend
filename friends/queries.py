
from django.db import connections
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from datetime import datetime
import pytz
from django.db import connections

def getTotalFriends(account_id):
    try:
        query = f"""
            SELECT COUNT(*) AS total_friends
            FROM glow.friends_friend
            WHERE status = 'Friends' AND (user_id = %s OR friend_id = %s);
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (account_id))
        result = cursor.fetchone()
        return result[0] if result else 0 

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def getFriendList(account_id):
    try:
        query = f"""
            SELECT * AS total_friends
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

def addFriend(friend_id, user_id):
    try:
        now = datetime.now(pytz.utc)
        status = "Pending"

        connection = connections["default"]
        cursor = connection.cursor()

        friend_query = """
            INSERT INTO glow.glow.friends_friend (status, date_friend_request, friend_id, user_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(friend_query, (status, now, friend_id, user_id))
        friend_request_id = cursor.fetchone()[0]

        notif_type_query = """
            SELECT id FROM glow.glow.notifications_notificationtype WHERE type = %s LIMIT 1
        """
        cursor.execute(notif_type_query, ("friend_request",))
        notif_type_id = cursor.fetchone()
        if not notif_type_id:
            raise Exception("Notification type 'friend_request' not found.")
        notif_type_id = notif_type_id[0]

        user_name_query = "SELECT firstname FROM glow.glow.accounts_account WHERE id = %s"
        cursor.execute(user_name_query, (user_id,))
        user_name = cursor.fetchone()[0] or "Someone"

        notif_content = f"{user_name} sent you a friend request"

        notif_query = """
            INSERT INTO glow.glow.notifications_notification (status, notif_type_id, notif_to_id, notif_from_id, content, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            notif_query,
            ("Unread", notif_type_id, friend_id, user_id, notif_content, now),
        )

        connection.commit()
        return {"status": "success", "message": "Friend request sent successfully."}

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()


def cancelFriendRequest(friend_id, user_id):
    try:
        connection = connections["default"]
        cursor = connection.cursor()

        delete_query = """
            DELETE FROM glow.glow.friends_friend 
            WHERE ((friend_id = %s AND user_id = %s) OR (friend_id = %s AND user_id = %s))
              AND status = 'Pending'
        """
        cursor.execute(delete_query, (friend_id, user_id, user_id, friend_id))

        delete_notif_query = """
            DELETE FROM glow.glow.notifications_notification
            WHERE ((notif_to_id = %s AND notif_from_id = %s) OR (notif_to_id = %s AND notif_from_id = %s))
              AND status = 'Unread'
        """
        cursor.execute(delete_notif_query, (friend_id, user_id, user_id, friend_id))

        connection.commit()
        return {
            "status": "success",
            "message": "Friend request canceled or removed.",
        }

    except Exception as error:
        print(f"Error canceling friend request: {error}")
        return {
            "status": "error",
            "message": "An error occurred while canceling the friend request.",
        }

    finally:
        if cursor:
            cursor.close()


def acceptFriend(friend_id, user_id):
    try:
        connection = connections["default"]
        cursor = connection.cursor()

        update_query = """
            UPDATE glow.glow.friends_friend 
            SET status = 'Friends'
            WHERE friend_id = %s AND user_id = %s AND status = 'Pending'
        """
        cursor.execute(update_query, (user_id, friend_id)) 

        connection.commit()
        return {
            "status": "success",
            "message": "Friend request accepted.",
        }

    except Exception as error:
        print(f"Error accepting friend request: {error}")
        return {
            "status": "error",
            "message": "An error occurred while accepting the friend request.",
        }

    finally:
        if cursor:
            cursor.close()

def unfriend(friend_id, user_id):
    try:
        connection = connections["default"]
        cursor = connection.cursor()

        delete_query = """
            DELETE FROM glow.glow.friends_friend
            WHERE (friend_id = %s AND user_id = %s) OR (friend_id = %s AND user_id = %s)
        """
        cursor.execute(delete_query, (friend_id, user_id, user_id, friend_id))

        connection.commit()
        return {
            "status": "success",
            "message": "You are no longer friends.",
        }

    except Exception as error:
        print(f"Error unfriending: {error}")
        return {
            "status": "error",
            "message": "An error occurred while unfriending.",
        }

    finally:
        if cursor:
            cursor.close()

def checkUserFriendRequest(friend_id, accId):
    try:
        #Dheck if there is any friend request between two users
        # It checks both directions:
        # (1) If user A sent a request to user B
        # (2) If user B sent a request to user A
        query = """
            SELECT * FROM glow.glow.friends_friend 
            WHERE (friend_id = %s AND user_id = %s)
               OR (friend_id = %s AND user_id = %s)
        """
        connection = connections["default"]
        cursor = connection.cursor()
        cursor.execute(query, (friend_id, accId, accId, friend_id))
        row = cursor.fetchone()

        if row is None:
            return None 
        
        result = {
            cursor.description[i][0]: value if value is not None else ""
            for i, value in enumerate(row)
        }

        return result

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
