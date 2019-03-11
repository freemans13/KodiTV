import json
import mysql.connector
import time
from pygtail import Pygtail
import os

def read_logs(line_processor):
    txt_files = []
    file_name = ""
    while True:
        if len(txt_files) == 0:
            # see https://stackoverflow.com/questions/5640630/array-filter-in-python
            txt_files = [entry for entry in os.listdir("event_logs/") if entry.endswith('.txt')]
            txt_files.sort()
            if file_name != "":
                # we know the last file_name we processed - no point re-loading older files
                txt_files = [file for file in txt_files if file > file_name]
        if len(txt_files) > 0:
            # grab oldest file in the array (first element) and remove it from the array
            file_name = txt_files.pop(0)
        if file_name == "":
            time.sleep(1)
        else:
            # print(file_name)

            connection = mysql.connector.connect(user='root', database='koditv')
            cursor = connection.cursor()

            for line in Pygtail("event_logs/" + file_name, offset_file="event_logs/" + file_name + "." + os.path.basename(__file__) + ".offset"):
                log_dict = json.loads(line)
                line_processor(connection, cursor, log_dict)

            cursor.close()
            connection.close()

            time.sleep(5)
