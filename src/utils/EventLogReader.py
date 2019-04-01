import json
import time
from pygtail import Pygtail
import os
import src.parameters as parameters


class EventLogReader:
    """
    This is a base class
    any class that extends this class must override the on-event method

    reads the log file line-by-line, for every line calls on_event method
    when we get to the end of a file, we look for the next file.
    If we cant find a new file we wait 5 seconds and look again

    """
    def __init__(self, offset_name):
        self.offset_name = offset_name
        self.previous_event_dict = None

    def start(self):
        """
        Start reading files and for every line read call on-event method

        :return: None
        """
        txt_files = []
        file_name = ""
        while True:
            if len(txt_files) == 0:
                txt_files = []
                for entry in os.listdir(parameters.EVENT_LOG_PATH):
                    # only interested in .txt files
                    if entry.endswith('.txt'):
                        # we know the last file_name we processed - no point re-loading older files
                        if file_name == "" or entry > file_name:
                            # add unprocessed file to array
                            txt_files.append(entry)

                txt_files.sort()
            if len(txt_files) > 0:
                # grab oldest file in the array (first element) and remove it from the array
                file_name = txt_files.pop(0)

            if file_name == "":
                # we don't have a file to read! try again in a second, rather than hog CPU
                time.sleep(1)
            else:

                for line in Pygtail(parameters.EVENT_LOG_PATH + file_name,
                                    offset_file=parameters.EVENT_LOG_PATH + file_name + "." + self.offset_name + ".offset"):
                    event_dict = json.loads(line)
                    self.on_event(event_dict)
                    self.previous_event_dict = event_dict

                # we finished reading the file, take a break before repeating process
                time.sleep(5)

    def on_event(self, event_dict):
        pass
