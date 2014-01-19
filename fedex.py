import requests
import json

class FedexTracker(object):

    def __init__(self, tracking_number):
      self.tracking_number = tracking_number
      self.create_request_data()
      self.make_request()

    def create_request_data(self):
        self.request_data = {
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
                            'trackingNumber': self.tracking_number,
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

    def make_request(self):
        self.rawData = requests.post('https://www.fedex.com/trackingCal/track', self.request_data).json()

    def last_location(self):
        return self.rawData["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["scanLocation"]

    def last_checkin(self):
        return self.rawData["TrackPackagesResponse"]["packageList"][0]["scanEventList"][0]["date"]

