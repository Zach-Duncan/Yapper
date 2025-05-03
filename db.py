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
            host="jlg7sfncbhyvga14.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
            user="hzlg5whgg9yl0z2d",
            password="k5ojwdzh9ehc3i3f",
            database="ouhpgoxvycbb2hpf",
            port=3306
        )
