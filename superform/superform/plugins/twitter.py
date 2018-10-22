import json
import twitter
import datetime

import datetime

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["consumer_key","consumer_secret","access_token_key","access_token_secret"]

def is_valid_tweet(tweet):
    '''
    Verify if the message respects Twitter's status (a.k.a tweet) conditions
    :param tweet: (string) the message the user wants to publish in Twitter
    :return: True if the message is a valid tweet, else False
    '''
    if len(tweet) > 280:
        return False
    else:
        return True

def is_time_to_publish(publishing) :
    date=publishing.date_from
    return  date <= datetime.datetime.now()


def run(publishing,channel_config):
    json_data = json.loads(channel_config)
    api = twitter.Api(consumer_key = json_data['consumer_key'],
                      consumer_secret = json_data['consumer_secret'],
                      access_token_key = json_data['access_token_key'],
                      access_token_secret = json_data['access_token_secret'])
    tweet = publishing.description



    if publishing.link_url :
        tweet = tweet + ' ' + publishing.link_url

    if is_valid_tweet(tweet) and is_time_to_publish(publishing): # For the moment, we avoid the tweet if it's not valid
        api.PostUpdate(tweet)
