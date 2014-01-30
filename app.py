import json
from flask import Flask
from flask import request
from flask import render_template
from bearclaw.fedex import FedexTracker
from bearclaw.packmule import PackMule

app = Flask(__name__)
packmule = PackMule()

@app.route("/")
def root():
    raw_entries = packmule.inventory()
    fedex_tracker = FedexTracker(raw_entries)
    fedex_tracker.execute()
    entries = fedex_tracker.entries
    return render_template('index.html', entries=entries)

@app.route("/create", methods=['POST'])
def create():
    data = json.loads(request.data)
    packmule.saddle_up(data)
    return "ok"

@app.route("/delete", methods=["DELETE"])
def delete():
    data = json.loads(request.data)
    number = int(data["number"])
    packmule.remove_entry(number)
    return "ok"

if __name__ == "__main__":
  app.run(debug=True)
