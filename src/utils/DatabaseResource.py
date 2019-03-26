import mysql.connector
import src.parameters as parameters


class DatabaseResource:
    """
    Establishes database connection
    allows reuse of same connection and cursor
    """
    def __init__(self):
        self.connection = mysql.connector.connect(user=parameters.DB_USER, database=parameters.DB_NAME)
        # https://stackoverflow.com/questions/21974627/mysql-connector-not-showing-inserted-results
        self.connection.start_transaction(isolation_level='READ COMMITTED')
        self.cursor = self.connection.cursor()

    def __del__(self):
        try:
            self.cursor.close()
        except ReferenceError:
            pass
        self.connection.close()
