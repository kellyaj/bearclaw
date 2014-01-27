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

    def saddle_up(self, entry):
        if self.is_not_duplicate(entry):
            with open("numbers.csv", "ab") as csvfile:
                csvfile.write("{0},{1},\n".format(entry["name"], entry["number"]))

    def is_not_duplicate(self, new_entry):
        entries = self.inventory()
        for entry in entries:
            if entry["number"] == new_entry["number"]:
                return False
