import mysql.connector


class DatabaseResource:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root', database='koditv')
        self.cursor = self.connection.cursor()

