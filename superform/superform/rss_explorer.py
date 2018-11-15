import ast
import datetime
import os
import feedparser
from flask import Blueprint, current_app, url_for, request, redirect, \
    render_template

from superform.models import db, Channel
from superform.plugins.LinkedIn import linkedin_plugin, \
    linkedin_code_processing
from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name

rss_explorer_page = Blueprint('rss_explorer', __name__)

@rss_explorer_page.route("/rss_explorer", methods = ['GET','POST'])
# @login_required(admin_required = True)
def feed_list():
    rfeeds = list()
    rss_dir = os.path.dirname(__file__) + "/plugins/rss"
    for xmlFile in os.listdir(rss_dir):
        print(xmlFile[len(xmlFile)-4:])
        if xmlFile[len(xmlFile)-4:] == ".xml":
            print(xmlFile)
            d = feedparser.parse(rss_dir+"/"+xmlFile)
            print(d)
            rtitle = d['feed']['title']
            rdescription = d['feed']['description']
            rlink = d['feed']['link']
            xmlpath = rlink.split('/')
            xmlpath = '/'.join(xmlpath[len(xmlpath)-2:])
            print(xmlpath," ##")
            print(rlink[14:])
            feed = [rtitle,rdescription,xmlpath]
            rfeeds.append(feed)
    return render_template("rss_explorer.html", feeds = rfeeds)


