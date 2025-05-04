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
            SELECT t.id, t.title, t.description
            FROM topics t
            JOIN subscriptions s ON t.id = s.topic_id
            WHERE s.user_id = %s
        """, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def create(title, user_id, description):
        db = DBConnection.get_connection()
        cursor = db.cursor()

        # Insert into topics with title, description, and access_count
        cursor.execute("""
            INSERT INTO topics (title, description, access_count) 
            VALUES (%s, %s, %s)
        """, (title, description, 0))

        topic_id = cursor.lastrowid

        # Automatically subscribe the user who created the topic
        cursor.execute("""
            INSERT INTO subscriptions (user_id, topic_id) 
            VALUES (%s, %s)
        """, (user_id, topic_id))

        db.commit()

        return topic_id
