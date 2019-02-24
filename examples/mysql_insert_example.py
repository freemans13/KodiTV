from datetime import date
import mysql.connector

connection = mysql.connector.connect(user='root', database='koditv')
cursor = connection.cursor()

add_history_record = ("INSERT INTO history "
                      "(date, title, channel, channelid) "
                      "VALUES (%s, %s, %s, %s)")

data = (date.today(), 'Only fools and horses', 'ITV1', '77')

# Insert new history record
cursor.execute(add_history_record, data)

# Make sure data is committed to the database
connection.commit()

cursor.close()
connection.close()