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

    @staticmethod
    def get_by_id(topic_id):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM topics WHERE id = %s", (topic_id,))
        return cursor.fetchone()

    @staticmethod
    def is_user_subscribed(user_id, topic_id):
        db = DBConnection.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1 FROM subscriptions WHERE user_id = %s AND topic_id = %s", (user_id, topic_id))
        return cursor.fetchone() is not None

    @staticmethod
    def get_subscribers(topic_id):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.username
            FROM users u
            JOIN subscriptions s ON u.id = s.user_id
            WHERE s.topic_id = %s
        """, (topic_id,))
        return cursor.fetchall()

    @staticmethod
    def increment_access_count(topic_id):
        db = DBConnection.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE topics 
            SET access_count = access_count + 1 
            WHERE id = %s
        """, (topic_id,))
        db.commit()
