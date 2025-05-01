import mysql.connector

class DBConnection:
    _instance = None

    @staticmethod
    def get_connection():
        if DBConnection._instance is None:
            DBConnection()
        return DBConnection._instance

    def __init__(self):
        if DBConnection._instance is not None:
            return
        DBConnection._instance = mysql.connector.connect(
            host="CaptainSpatula.mysql.pythonanywhere-services.com",
            user="CaptainSpatula",
            password="Caliber2020!@#",
            database="CaptainSpatula$Yapper"
        )
