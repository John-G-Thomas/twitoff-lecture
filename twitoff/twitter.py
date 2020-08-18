"""Retrieve Tweets, embeddings, and persist in the database."""
import basilica
import tweepy
from .models import DB, Tweet, User

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']
# TODO don't have raw secrets in the code, move to .env!
TWITTER_API_KEY = 'eSRNPlZyihxrgNXY4nsKDEeGc'
TWITTER_API_SECRET_KEY = 'cXdR42US7xoIqWs2W6cC0bAzOzGezhBOkng9P8jEXc9TB7x0Ff'
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    """Add or update a user and their Tweets, error if not a Twitter user."""
    twitter_user = TWITTER.get_user(username)
    db_user = (User.query.get(twitter_user.id) or
               User(id=twitter_user.id, name=username))
    DB.session.add(db_user)
    # Lets get the tweets - focusing on primary (not retweet/reply)
    tweets = twitter_user.timeline(
        count=200, exclude_replies=True, include_rts=False,
        tweet_mode='extended'
    )
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300])
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)
    DB.session.commit()
