import json
import twitter

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["consumer_key","consumer_secret","access_token_key","access_token_secret"]

def tweet_too_big(tweet):
    '''
    Verify if the message respects Twitter's limitation of characters
    :param tweet: (string) the message the user wants to publish in Twitter
    :return: True if the message is longer than 280 characters, False otherwise
    '''
    if len(tweet) > 280:
        return True
    else:
        return False


def run(publishing,channel_config):
    try:
        json_data = json.loads(channel_config)

        api = twitter.Api(consumer_key = json_data['consumer_key'],
                  consumer_secret = json_data['consumer_secret'],
                  access_token_key = json_data['access_token_key'],
                  access_token_secret = json_data['access_token_secret'])
    except json.decoder.JSONDecodeError  as e:
        return "uncorrect credentials"


    tweet = publishing.description



    if publishing.link_url :
        tweet = tweet + ' ' + publishing.link_url
    if tweet_too_big(tweet): # For the moment, we avoid the tweet if it's not valid
        api.PostUpdates(status=publishing.description, continuation="[...]")
    else :
        api.PostUpdate(status = publishing.description)