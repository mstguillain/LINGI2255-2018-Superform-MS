import sys
sys.path.append("..")
from plugins.facebook_plugin import *
import unittest

class FacebookTest(unittest.TestCase):
    def test_publish(self):
        msg = "Test d'une publication !!!"
        cfg = {
            "page_id"      : "285844238930581",  # Step 1
            "access_token" : "EAAHcEGT1yyEBAOSo50WUiM0563zVZCxnZCdd2XVJRAll0wIFztF4m1pPfw5hqlDwbvqZBCMNlnqzlTZC2RSkzDSTzwJZBhJuyZBcyAIgyIiSBqEZBV4GbyVhKJLWlCuZByRyn6AxgTFtGMeJwEQqvBCjZCHGZBfb5qBy2H27x2z6dMygDbJiltxSZCRLMSYAWE4QYrUwLgQIVxUHgZDZD"   # Step 3
        }

        api = get_api(cfg)
        publication_id = publish(msg)
        pub = api.get_object(id=publication_id, fields='message')
        self.assertEqual(msg, pub['message'])
        delete(publication_id)
 
if __name__ == '__main__':
    unittest.main()
