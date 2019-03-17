from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def query_with_fetchone():
    try:
        # dbconfig = read_db_config()
        # conn = MySQLConnection(**dbconfig)
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM books")
        with open('event_logs/2019-02-17.txt') as file:
            # row = cursor.fetchone()
            row = file.readline()

            while row:
                print(row)
                row = file.readline()

    except Error as e:
        print(e)

    finally:
        # cursor.close()
        # conn.close()


if __name__ == '__main__':
    query_with_fetchone()