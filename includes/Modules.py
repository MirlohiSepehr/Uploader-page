#------------------------- Imports ------
import json
from re import S


#------------- Classes explanation


class WorkWithFiles:

    def __init__(self, filename):
        self.filename = filename

    def give_content(self):
        open_r = open(f"database/{self.filename}.json", 'r')
        return json.load(open_r)

    def save_content(self, data):
        open_w = open(f"database/{self.filename}.json", 'w')
        json.dump(data, open_w)

    def add_content(self, data):
        open_r = open(f"database/{self.filename}.json", 'r')
        file_to_read = json.load(open_r)
        file_to_read.append(data)
        open_w = open(f"database/{self.filename}.json", 'w')
        json.dump(file_to_read, open_w)

    # def close_file(self):
    #     self.open_r.close()
    #     # self.open_w.close()
