import tweepy
import logging
import sys
import config
import json
# Authenticate to Twitter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    auth = tweepy.OAuthHandler("bHqVLJG8G3i6httnaJbpMimKo",
                               "wuQ3dAn7bd7YYUqrY3hKjsgWDMTEbMA3tnfy1FZYiMJ1aZiwMD")
    auth.set_access_token("1378484568236384262-pFj61W7dYrYdKYxBouWQLqxSeDuI6T",
                          "a6jpahDbpTwNOVU6Je0FkUS5N8w2cXxRDDTkEO9uHkGqy")
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["#ViscaElBarca", "#viscaelbarca"])
