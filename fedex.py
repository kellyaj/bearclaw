import requests
import json
import re

class FedexTracker(object):

    def __init__(self, tracking_numbers):
      self.tracking_numbers = tracking_numbers
      self.request_datas = []
      self.raw_data_responses = []
      self.entries = []
      self.create_request_data()
      self.make_request()
      self.generate_entry_dictionary()

    def create_request_data(self):
      for number in self.tracking_numbers:
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
                              'trackingNumber': number,
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
          self.request_datas.append(data)

    def make_request(self):
        for request_data in self.request_datas:
            self.raw_data_responses.append(requests.post('https://www.fedex.com/trackingCal/track', request_data).json())

    def last_location(self, raw_data):
        return raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["scanLocation"]

    def last_checkin(self, raw_data):
        raw_date = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["date"]
        raw_time = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["time"]
        date = self.format_date(raw_date)
        time = self.format_time(raw_time)
        return "{0} at {1}".format(time,date)

    def format_date(self, raw_date):
        split_date = raw_date.split("-")
        return "{0}/{1}/{2}".format(split_date[1], split_date[2], split_date[0])

    def format_time(self, raw_time):
        split_time = raw_time.split(":")
        return "{0}:{1}".format(split_time[0], split_time[1])

    def generate_entry_dictionary(self):
        for raw_data in self.raw_data_responses:
            entry = {}
            entry['last_location'] = self.last_location(raw_data)
            entry['last_checkin'] = self.last_checkin(raw_data)
            entry['out_for_delivery'] = self.get_delivery_status(raw_data)
            self.entries.append(entry)

    def is_out_for_delivery(self, raw_data):
        status = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["status"]
        return re.match(status, "delivery", re.IGNORECASE) is not None

    def has_been_delivered(self, raw_data):
        status = raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["status"]
        return re.match(status, "delivered", re.IGNORECASE) is not None

    def get_delivery_status(self, raw_data):
        if self.is_out_for_delivery(raw_data):
            return "OFD"
        elif self.has_been_delivered(raw_data):
            return "Delivered"

