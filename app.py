from flask import Flask
from flask import request
from flask import render_template
from fedex import FedexTracker
app = Flask(__name__)

@app.route("/")
def root():
    nums = ["9611804258025804723257", "9611804258025804723257", "9611804183634603474634", "123456789012"]
    fedex_tracker = FedexTracker(nums)
    return render_template('index.html', entries=fedex_tracker.entries)

@app.route("/create", methods=['POST'])
def create():
    with open("numbers.csv", "ab") as fo:
        fo.write(request.data + "\n")
    return "ok"


if __name__ == "__main__":
  app.run(debug=True)
