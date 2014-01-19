from flask import Flask
from fedex import FedexTracker
app = Flask(__name__)

@app.route("/")
def root():
    fedex_tracker = FedexTracker("9611804258025804723257")
    return_data = fedex_tracker.last_location() + " on " + fedex_tracker.last_checkin()
    return return_data

if __name__ == "__main__":
  app.run(debug=True)
