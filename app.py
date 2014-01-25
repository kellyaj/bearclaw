import csv
import json
from flask import Flask
from flask import request
from flask import render_template
from fedex import FedexTracker
app = Flask(__name__)

@app.route("/")
def root():
    raw_entries = []
    with open("numbers.csv", "rb") as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        raw_entry = {}
        raw_entry["name"] = row[0]
        raw_entry["number"] = row[1]
        raw_entries.append(raw_entry)
    del raw_entries[0]
    fedex_tracker = FedexTracker(raw_entries)
    entries = fedex_tracker.raw_entries
    return render_template('index.html', entries=entries)

@app.route("/create", methods=['POST'])
def create():
    data = json.loads(request.data)
    with open("numbers.csv", "ab") as fo:
        fo.write("{0},{1},\n".format(data["name"], data["number"]))
    return "ok"


if __name__ == "__main__":
  app.run(debug=True)
