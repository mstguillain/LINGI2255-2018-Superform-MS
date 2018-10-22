import facebook
from flask import current_app
import json

FIELDS_UNAVAILABLE = ['Title','Description']

CONFIG_FIELDS = ["sender","receiver"]

def run(publishing,channel_config):
    #json_data = json.loads(channel_config)

    # Fill in the values noted in previous steps here
    cfg = {
    "page_id"      : "285844238930581",  # Step 1
    "access_token" : "EAAHcEGT1yyEBAHfHfxCjN5Fj8YRQ9ygvqCtBzQFBEYOdLe9YmSZCfwQUHPsfNhBI51MZBPZBoX7GIcyCswOZBwMQIycmeeLTNoOrxMjiqjOjZCWoidaPe4ZCFiLAThoZCWXFc1SSjQkfz11v8kXwxUBMZA9qftCa3XFhZCElVVd9i7UE8UW0LueDdHW007hPhNffjgXGXiH5v558ZBKYGfEeCpBKb4mzn3vy4ZD"   # Step 3
    }

    api = get_api(cfg)
    #msg a custom, choper le contenu du champ dans le post 
    
    #On chope le message dans le champ description du post.
    body = publishing.description
    #msg = "Hello, world!" 
    status = api.put_object(parent_object='me',connection_name='feed',message=body)

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