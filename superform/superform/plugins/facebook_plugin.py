import facebook
from flask import current_app, session
from superform.models import db, User
import json

FIELDS_UNAVAILABLE = ['Title','Description']

CONFIG_FIELDS = ["sender","receiver"]

CFG = {
        "page_id"      : "285844238930581",  # Step 1
        "access_token" : "EAAHcEGT1yyEBAHhR2TqDm5tbTtuX7pCFMPcLC6xW4bEFAaXjN43pDEoiuzhUr5X9YT8cVYjP2hxu6cJBJrgBMipMO7JmAI06FEgPcVD0ZCkBimOYwts8Wl4KqZAZBOekYdvtZBWWK2fuJ8XTFkLPvit3Ulm8S9X0OOvRomOr35f7ZCZAnFeYdH4U2V7WTyDpimraZA7xLw5PABb4RZC35zEO"
    }
    

def run(publishing, channel_config):
    api = get_api(CFG)
    #user_string_tokens = db.session.query(User).filter(User.id==session.get("fb_cred",""))
    #Acces à la base de donnée pour récuperer les differents couples page_id|page_access_token_rallongé
    #verify this request
    user = User.query.get(session.get("fb_cred", ""))
    print("==============================================")
    print(user)
    print("==============================================")

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