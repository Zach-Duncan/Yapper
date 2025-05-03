from db import DBConnection

class User:
    @staticmethod
    def register(username, password):
        db = DBConnection.get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        db.commit()

    @staticmethod
    def login(username, password):
        db = DBConnection.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
        return cursor.fetchone()