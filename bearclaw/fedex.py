import requests
import json
import re

class FedexTracker(object):

    def __init__(self, raw_entries):
        self.entries = raw_entries
        self.create_request_data()

    def execute(self):
        self.make_request()
        self.update_entries()

    def create_request_data(self):
        for entry in self.entries:
            data = {
                'data': json.dumps({
                    'TrackPackagesRequest': {
                        'appType': 'wtrk',
                        'uniqueKey': '',
                        'processingParameters': {
                            'anonymousTransaction': True,
                            'clientId': 'WTRK',
                            'returnDetailedErrors': True,
                            'returnLocalizedDateTime': False
                            },
                        'trackingInfoList': [{
                            'trackNumberInfo': {
                                'trackingNumber': entry["number"],
                                'trackingQualifier': '',
                                'trackingCarrier': ''
                                }
                            }]
                        }
                    }),
                'action': 'trackpackages',
                'locale': 'en_US',
                'format': 'json',
                'version': 99
            }
            entry["request_data"] = data

    def make_request(self):
        for entry in self.entries:
            entry["raw_data_response"] = requests.post('https://www.fedex.com/trackingCal/track', entry["request_data"]).json()

    def last_location(self, raw_data):
        return raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["scanLocation"]

    def last_checkin(self, raw_data):
        raw_date = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["date"]
        raw_time = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["time"]
        return "{0} on {1}".format(self.format_time(raw_time),self.format_date(raw_date))

    def format_date(self, raw_date):
        split_date = raw_date.split("-")
        return "{0}/{1}/{2}".format(split_date[1], split_date[2], split_date[0])

    def format_time(self, raw_time):
        split_time = raw_time.split(":")
        return "{0}:{1}".format(split_time[0], split_time[1])

    def update_entries(self):
        for entry in self.entries:
            raw_data = entry["raw_data_response"]
            entry['last_location'] = self.last_location(raw_data)
            entry['last_checkin'] = self.last_checkin(raw_data)
            entry['status'] = self.get_status_text(raw_data)
            del entry["raw_data_response"]
            del entry["request_data"]

    def is_out_for_delivery(self, raw_data):
        status = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["status"]
        return re.match(status, "delivery", re.IGNORECASE) is not None

    def has_been_delivered(self, raw_data):
        status = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["status"]
        return re.match(status, "delivered", re.IGNORECASE) is not None

    def get_status_text(self, raw_data):
        return raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["status"]

    def get_delivery_status(self, raw_data):
        if self.is_out_for_delivery(raw_data):
            return "OFD"
        elif self.has_been_delivered(raw_data):
            return "Delivered"
        else:
            return self.get_status_text(raw_data)

