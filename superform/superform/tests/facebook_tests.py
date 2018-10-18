import sys
sys.path.append("..")
from plugins.facebook_plugin import *
import unittest

class FacebookTest(unittest.TestCase):
    def test_publish(self):
        msg = 'Ceci est une publication !'
        cfg = {
            "page_id"      : "285844238930581",  # Step 1
            "access_token" : "EAAHcEGT1yyEBAOrJr07ZC71bLrPryUUY2luLaLgC7jrycFDLbJ857W3RVLvIru0Sh8WyR4Udr8YA2OCtDDEWEtJrNoBKYMTZAjIMwZAW9ZAtaLvh76cX7xCZBrBFEq3w2B7NdjCPI2z7tAiyGzZCaLsFx4mPyFoSQZCkYCnbaXOpAZDZD"   # Step 3
        }

        api = get_api(cfg)
        publication_id = publish(msg)
        pub = api.get_object(id=publication_id, fields='message')
        self.assertEquals(msg, pub['message'])
        delete(publication_id)

if __name__ == '__main__':
    unittest.main()