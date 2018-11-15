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
# https://www.pmwiki.org/wiki/PmWiki/Passwords

# éditer une page sur wiki :
# https://www.pmwiki.org/wiki/PmWiki/BasicEditing

# à faire :
# - rajouter :  image_url, connexion avec user et password
# - gerer accent dans desciption

# COMMENT ON A GERE L'AUTHENTIFICATION POUR LE MOMENT :
# On modifie les accès de notre server local pour que seules les personnes
# possédant le mot de passe puissent créer un nouveau post.
#
#       * Modifier accès server local :
#           --> http://localhost/pmwiki-2.2.109/pmwiki.php?n=News.GroupAttributes?action=attr
#           --> mettre un mot de passe pour le champ edit (par exemple "edit")
#               Dans cet exemple, il y aura donc besoin du mot de passe pour créer toutes les pages qui commencent par News. (ex: News.Conference)
#       * Configurer la channel wiki sur superform :
#           --> mettre le mot de passe choisi dans le champ password. Pour l'instant on peut mettre ce qu'on veut dans le champs username

FIELDS_UNAVAILABLE = ['Title','Description']
CONFIG_FIELDS = ["username","password"]


def makeText(publishing):
    titre = "!! " + publishing.title + "\n"
    try :
        author = publishing.get_author()
    except AttributeError:
        author = "Superform"
    except TypeError:
        author = "Superform"

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

    try:
        json_data = json.loads(channel_config)
        authid= json_data['username'] # à rajouter dans configuration de la channel sur superform sinon ne marche pas...
        authpw = json_data['password'] # à rajouter dans configuration de la channel sur superform sinon ne marche pas...
    except json.decoder.JSONDecodeError  as e:
        return "error json decoder"

    pageName = "News."+str(publishing.title).replace(" ","")
    text = makeText(publishing)
    data = {"n": pageName, "text": text, "action": "edit", "post": "1", 'authid': authid, "authpw":authpw,"basetime": math.floor(time.time())}
    # r2 = requests.post("http://localhost/pmwiki-2.2.109/pmwiki.php?n=Main.Essai_nono&action=edit&text=Hello%20World&post=1", data)

    r2 = requests.post("http://localhost/pmwiki-2.2.109/pmwiki.php", data)



