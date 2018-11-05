import json
import twitter


CONFIG_FIELDS = ["username","password"]



def run(publishing,channel_config):
    json_data = json.loads(channel_config)
    #TODO completer

    #api = twitter.Api(consumer_key = json_data['consumer_key'],
     #                 consumer_secret = json_data['consumer_secret'],
      #                access_token_key = json_data['access_token_key'],
       #               access_token_secret = json_data['access_token_secret'])
    #tweet = publishing.description
    #if is_valid_tweet(tweet): # For the moment, we avoid the tweet if it's not valid
     #   api.PostUpdate(publishing.description)

