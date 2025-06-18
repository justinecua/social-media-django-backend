
from django.db import connections
from posts.queries import time_ago
from datetime import datetime

def countNotifications(account_id):
    try:
        query = f"""
                SELECT COUNT(*) FROM glow.glow.notifications_notification
                WHERE notif_to_id = %s
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



def showNotificationsByUser(account_id):
    try:
        query = f"""
                SELECT * FROM glow.glow.notifications_notification
                WHERE notif_to_id = %s
                """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (account_id,))

        results = [
            dict(
                (cursor.description[i][0], value if value is not None else "")
                for i, value in enumerate(row)
            )
            for row in cursor.fetchall()
        ]
        for notif in results:
            if "created_at" in notif and isinstance(notif["created_at"], datetime):
                notif["created_at"] = time_ago(notif["created_at"])

        return results

    except Exception as error:
        print(f"Error: {error}")
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()