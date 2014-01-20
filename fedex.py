import requests
import json

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
        return raw_data["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["date"]

    def generate_entry_dictionary(self):
        for raw_data in self.raw_data_responses:
            entry = {}
            entry['last_location'] = self.last_location(raw_data)
            entry['last_checkin'] = self.last_checkin(raw_data)
            self.entries.append(entry)
