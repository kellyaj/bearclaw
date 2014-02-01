import unittest
from bearclaw.fedex import FedexTracker

class FedexTrackerTests(unittest.TestCase):

    def setUp(self):
        self.fake_raw_data = {
            u'TrackPackagesResponse': {
              u'packageList': [{
                u'scanEventList': [
                  {
                    u'status': u'Delivered',
                    u'time': u'11:17:10',
                    u'date': u'2014-01-02',
                    u'scanLocation': u'Chicago, IL'
                  }
                ]
              }]
            }
          }
        self.entry = {"name": "fake item", "number": "1234567890", "raw_data_response": self.fake_raw_data}
        self.fedex_tracker = FedexTracker([self.entry])

    def test_format_date(self):
        raw_date = "2014-01-02"
        self.assertEqual(self.fedex_tracker.format_date(raw_date), "01/02/2014")

    def test_format_time(self):
        raw_time = "11:17:10"
        self.assertEqual(self.fedex_tracker.format_time(raw_time), "11:17")

    def test_last_location(self):
        raw_data = self.entry["raw_data_response"]
        self.assertEqual(self.fedex_tracker.last_location(raw_data), "CHICAGO, IL")

    def test_last_checkin(self):
        raw_data = self.entry["raw_data_response"]
        expected_date_time = "11:17 ON 01/02/2014"
        self.assertEqual(self.fedex_tracker.last_checkin(raw_data), expected_date_time)

    def test_getting_status_text(self):
        raw_data = self.entry["raw_data_response"]
        self.assertEqual(self.fedex_tracker.get_status_text(raw_data), "DELIVERED")

    def test_entry_updating(self):
        self.fedex_tracker.update_entries()
        revised_entry = self.fedex_tracker.entries[0]
        self.assertEqual(revised_entry["last_location"], "CHICAGO, IL")
        self.assertEqual(revised_entry["last_checkin"], "11:17 ON 01/02/2014")
        self.assertEqual(revised_entry["status"], "DELIVERED")
