import facebook
from flask import current_app
import json
import time

FIELDS_UNAVAILABLE = ['Title','Description']

CONFIG_FIELDS = ["sender","receiver"]
CFG = {
        "page_id"      : "285844238930581",  # Step 1
        "access_token" : "EAAHcEGT1yyEBAMMmOCYrWGJAfJZCmlZAxlTc4hDNQ6HrW0r5Od65KrHDsAU2IzCWp2IqTp8JPXwgkbU3DvHRwfTj6j8uZBI4w4pvD0Lrma1cOE2oVTUm3PST9qpGzR2sgB6n8yCshzUSbDBbZA0hROfafsLRZB3M4XwDfoVrOOSS6SGZALizRriZBkZAsI2prtXf9jmVWiZCa3t5pl6DhLV2v"   # Step 3
    }

def run(publishing, channel_config):
    api = get_api(CFG)
    #msg a custom, choper le contenu du champ dans le post 
    
    #On chope le message dans le champ description du post.
    body = publishing.description
    #msg = "Hello, world!" 
    id = publish(body)


def publish(message):
    """ 
    Publie sur le compte et renvoie l'id de la publication
    """   
    api = get_api(CFG)
    status = api.put_object(parent_object='me', connection_name='feed', message=message)
    return status['id']

def delete(id):
    """
    Supprime la publication
    """ 
    api = get_api(CFG)
    api.delete_object(id)

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    # Get page token to post as the page. You can skip 
    # the following if you want to post as yourself. 
    """resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
        page_access_token = page['access_token']
        """
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph
    # You can also skip the above if you get a page token:
    # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
    # and make that long-lived token as in Step 3
