import sys
sys.path.append("..")
from plugins.facebook_plugin import *
import unittest
from urllib.request import urlopen

class FacebookTest(unittest.TestCase):
    def test_publish(self):
        msg = "This is a publication test"
        api = get_api(CFG)
        publication_id = publish(msg)
        pub = api.get_object(id=publication_id, fields='message')
        self.assertEqual(msg, pub['message'])
        delete(publication_id)

    def test_connectivity(self):
        try:
            response = urlopen('https://www.google.com/', timeout=10)
            return True
        except:
            return False
 
if __name__ == '__main__':
    unittest.main()
