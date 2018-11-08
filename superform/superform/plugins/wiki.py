import json
import requests
import time
import datetime
import math

# liens utiles :

# à propos de python et des requêtes http :
# http://dridk.me/python-requests.html
# http://docs.python-requests.org/en/master/api/ --> API de requests

# à propos de l'authentification sur pmwiki
# https://www.pmwiki.org/wiki/PmWikiFr/AuthUser

# éditer une page sur wiki :
# https://www.pmwiki.org/wiki/PmWiki/BasicEditing

# à faire :
# - rajouter : link_url (ok?), image_url, connexion avec user et password
# - gérer basetime
# - gérer nom de page (ok?)
# - gérer date (ok?)

FIELDS_UNAVAILABLE = []
CONFIG_FIELDS = ["username","password"]


def makeText(publishing):
    titre = "!! " + publishing.title + "\n"
    author = publishing.get_author()
    #date = str(publishing.date_from).split()[0]
    date = str(datetime.datetime.now().strftime("%d/%m/%Y"))

    suite = "Par " + author + " Publie le " + date +"\n"
    corps = str(publishing.description).replace("\n","[[<<]]") + "\n"

    text = titre + "-----" + suite + corps
    if len(str(publishing.link_url))>0 :
        link_url = "-----"+"[["+publishing.link_url+"]]"+"\n"
        text = text +  link_url
    image_url = publishing.image_url
    return text

def run(publishing,channel_config):
    json_data = json.loads(channel_config)
    authid= json_data['username'] # à rajouter dans configuration de la channel sur superform sinon ne marche pas...
    authpw = json_data['password'] # à rajouter dans configuration de la channel sur superform sinon ne marche pas...

    pageName = "News."+str(publishing.title).replace(" ","")
    text = makeText(publishing)
    data = {"n": pageName, "text": text, "action": "edit", "post": "1","basetime": math.floor(time.time())}
    # r2 = requests.post("http://localhost/pmwiki-2.2.109/pmwiki.php?n=Main.Essai_nono&action=edit&text=Hello%20World&post=1", data)

    r2 = requests.post("http://localhost/pmwiki-2.2.109/pmwiki.php", data)


    #TODO completer

    #api = twitter.Api(consumer_key = json_data['consumer_key'],
     #                 consumer_secret = json_data['consumer_secret'],
      #                access_token_key = json_data['access_token_key'],
       #               access_token_secret = json_data['access_token_secret'])
    #tweet = publishing.description
    #if is_valid_tweet(tweet): # For the moment, we avoid the tweet if it's not valid
     #   api.PostUpdate(publishing.description)

