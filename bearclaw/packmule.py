import csv

class PackMule(object):

    def __init__(self):
        self.csv_file = "numbers.csv"

    def inventory(self):
        entries = []
        with open(self.csv_file, "rb") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                entries.append({"name": row[0], "number": row[1]})
        return entries
