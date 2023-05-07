import tweepy
from config import TwitterConfig

class TwitterPostEvent:

    def __init__(self, event, image):
        self.event = event
        self.image = image
        # TODO generate text. just "title"?


class Twitter:

    def __init__(self, cfg: TwitterConfig):

        consumer_key = open(cfg.api_key_file).read()
        consumer_secret = open(cfg.api_key_secret_file).read()
        access_token = open(cfg.access_token_file).read()
        access_token_secret = open(cfg.access_token_secret_file).read()
        self.tweepy_client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )



    def post(self, post: TwitterPostEvent, answer=None):
        print("dont tweet now.")
        """
        response = self.tweepy_client.create_tweet(
            text="This Tweet was Tweeted using Tweepy and Twitter API v2!"
        )
        """
        pass

    def get_posted_tweet(self, id):
        pass