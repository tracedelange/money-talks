import tweepy
from config import twitter_config

consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_token_secret = twitter_config.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

data = api.rate_limit_status()

print(data['resources']['statuses']['/statuses/user_timeline'])
