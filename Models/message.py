from db import DBConnection

class Message:
    @staticmethod
    def post_message(user_id, topic_id, content):
        db = DBConnection.get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO messages (user_id, topic_id, content) VALUES (%s, %s, %s)",
                       (user_id, topic_id, content))
        db.commit()

    @staticmethod
    def get_recent_by_topic(topic_id, limit=2):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT messages.*, users.username
            FROM messages
            JOIN users ON messages.user_id = users.id
            WHERE topic_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (topic_id, limit))
        return cursor.fetchall()

    @staticmethod
    def get_all_by_topic(topic_id):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT messages.*, users.username
            FROM messages
            JOIN users ON messages.user_id = users.id
            WHERE topic_id = %s
            ORDER BY created_at DESC
        """, (topic_id,))
        return cursor.fetchall()

    @staticmethod
    def get_by_id(message_id):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM messages WHERE id = %s", (message_id,))
        return cursor.fetchone()

    @staticmethod
    def delete_message(message_id):
        db = DBConnection.get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        db.commit()
