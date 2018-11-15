from flask import current_app
import json
import rfeed
import datetime
import os
import feedparser

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = ["Feed title", "Feed description"]

RSS_DIR = "localhost:5000/rss/"

def newFeed(rname,rdescription):
    """
    :param rname: name for the RSS feed
    :param rdescription: description of the RSS feed
    :return: Will return a new (empty publication) feed with "localhost:5000/rss/NAME_OF_FEED.xml" as link
    """
    print("ici")
    temp = rname.split(" ")
    nameOfFeed = "_".join(temp)
    feedLink = RSS_DIR+nameOfFeed+".xml"
    feed = rfeed.Feed(
        title=rname,
        link=feedLink,
        description=rdescription,
        lastBuildDate=datetime.datetime.now(),
        docs=None,
        items=[])
    print("link: ",feedLink)
    return feed

def import_items(xml_path):
    """
    :param xml_path: the path to an existing xml file
    :return: return the list of all previous publication (items) on the feed.
    Since when we publish, we overwrite the xml file, we need the history of the publication to re-write them aswell.
    """
    items = list()
    d = feedparser.parse(xml_path)

    for post in d.entries:
        title = None
        link = None
        body = None
        date = None
        if 'title' in post:
            title = post.title
            # print('title ok')
        if 'link' in post:
            link = post.link
            # print('link ok')
        if 'description' in post:
            body = post.description
            # print('description ok')
        if 'published' in post:
            date= post.published
            # print('date ok')

        item = rfeed.Item(
            title=title,
            link=link,
            description=body,
            pubDate=datetime.datetime.strptime(date, "%a, %d %b %Y %X GMT"))
        items.append(item)
    return items

def run(publishing, channel_config):

    json_data = json.loads(channel_config)
    rname = json_data['Feed title']
    rdescription = json_data['Feed description']
    item_title = publishing.title
    item_body = publishing.description
    item_link = publishing.link_url
    item_from = publishing.date_from
    item_until = publishing.date_until
    item_img = publishing.image_url

    item = rfeed.Item(
        title=item_title,
        link=item_link,
        description=item_body,
        pubDate=item_from)


    localPath = os.path.dirname(__file__)+"/rss/feed_"+str(publishing.channel_id)+".xml"
    feed = newFeed(rname, rdescription)
    feed.items.append(item)
    if os.path.isfile(localPath): #import older publishing if any
        print("a file already exist")
        olderItems = import_items(localPath)
        print(olderItems)
        print(len(olderItems))
        feed.items.extend(olderItems)


    print(feed.items)
    with open(localPath, 'w') as f:
        a = feed.rss()
        f.write(a)


