import mysql.connector
import src.parameters as parameters


class DatabaseResource:
    def __init__(self):
        self.connection = mysql.connector.connect(user=parameters.DB_USER, database=parameters.DB_NAME)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
