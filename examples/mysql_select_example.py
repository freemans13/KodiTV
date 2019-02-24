import datetime
import mysql.connector

connection = mysql.connector.connect(user='root', database='koditv')
cursor = connection.cursor()

query = ("SELECT date, title, channel, channelid FROM history "
         "WHERE date BETWEEN %s AND %s")

start = datetime.date(2019, 2, 1)
end = datetime.date(2019, 3, 1)

cursor.execute(query, (start, end))


for (date, title, channel, channelid) in cursor:
    print(date, title, channel, channelid)

cursor.close()
connection.close()