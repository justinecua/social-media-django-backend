
from django.db import connections
from posts.queries import time_ago
from datetime import datetime, date

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
        query = """
            SELECT * FROM glow.glow.notifications_notification 
            LEFT JOIN glow.glow.accounts_account 
            ON notif_from_id = glow.glow.accounts_account.id
            WHERE notif_to_id = %s
        """
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(query, (account_id,))

        columns = [col[0] for col in cursor.description]
        results = []

        for row in cursor.fetchall():
            notif = {}
            for i, value in enumerate(row):
                col_name = columns[i]

                if col_name == "created_at" and isinstance(value, datetime):
                    notif[col_name] = time_ago(value)

                elif isinstance(value, (datetime, date)):
                    notif[col_name] = value.isoformat()

                elif value is None:
                    notif[col_name] = ""

                else:
                    notif[col_name] = value

            results.append(notif)

        return results

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
