import sys
sys.path.append("..")
<<<<<<< HEAD
from plugins.facebook import *
=======
from plugins.facebook_plugin import *
>>>>>>> 4b1d737f7bfd0426641483a9980ea33ff9f4aced
import unittest

class FacebookTest(unittest.TestCase):
    def test_publish(self):
        msg = "Test d'une publication"
        cfg = {
            "page_id"      : "285844238930581",  # Step 1
            "access_token" : "EAAHcEGT1yyEBAAMbUIDx31kDlC3zi8heSI84KWakZBwAaf4fRVnMPSNrZA47gsS2vzdOdq656mlvqVAdCb0kXK1hE4LH68x8MyDWWCZBgAmvCmPvmbIaI5TkgV3t4mvFPup40oCYmjS59e3OmKi4aos9TZAIBvazarZBZCMTD8pdNvWZAiZCRTmmuy198NEZC8vJOuMGGTygsHQZDZD"   # Step 3
        }

        api = get_api(cfg)
        publication_id = publish(msg)
        pub = api.get_object(id=publication_id, fields='message')
        self.assertEqual(msg, pub['message'])
        delete(publication_id)
 
if __name__ == '__main__':
<<<<<<< HEAD
    unittest.main()
=======
    unittest.main()
>>>>>>> 4b1d737f7bfd0426641483a9980ea33ff9f4aced
