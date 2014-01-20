from flask import Flask
from flask import render_template
from fedex import FedexTracker
app = Flask(__name__)

@app.route("/")
def root():
    fedex_tracker = FedexTracker(["9611804258025804723257"])
    return render_template('index.html', entries=fedex_tracker.entries)

if __name__ == "__main__":
  app.run(debug=True)
