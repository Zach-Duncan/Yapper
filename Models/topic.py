from db import DBConnection

class Topic:
    @staticmethod
    def get_all():
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM topics")
        return cursor.fetchall()

    @staticmethod
    def get_subscribed(user_id):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id, t.title 
            FROM topics t
            JOIN subscriptions s ON t.id = s.topic_id
            WHERE s.user_id = %s
        """, (user_id,))
        return cursor.fetchall()