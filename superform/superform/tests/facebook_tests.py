import sys
sys.path.append("..")
from plugins.facebook_plugin import *
import unittest

class FacebookTest(unittest.TestCase):
    def test_publish(self):
        msg = "Test d'une publication !!!"


        api = get_api(CFG)
        publication_id = publish(msg)
        pub = api.get_object(id=publication_id, fields='message')
        self.assertEqual(msg, pub['message'])
        delete(publication_id)
 
if __name__ == '__main__':
    unittest.main()
