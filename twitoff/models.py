"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # Tweet IDS are orinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_Tweet():
    """Example data to play with."""
    tweetauston1 = Tweet(id=1, text='Lambda school is amazing!', user_id=1, user='austen')
    tweetauston2 = Tweet(id=4, text='Lambda school is amazing!', user_id=1, user='austen')
    tweetauston3 = Tweet(id=6, text='Lambda school is amazing!', user_id=1, user='austen')
    tweetelon1 = Tweet(id=2, text='WE gonna Go TO Mars!', user_id=2, user='elonmusk')
    tweetelon2 = Tweet(id=3, text='WE gonna Go TO Mars!', user_id=2, user='elonmusk')
    tweetelon3 = Tweet(id=5, text='WE gonna Go TO Mars!', user_id=2, user='elonmusk')
    DB.session.add(tweetauston1)
    DB.session.add(tweetauston2)
    DB.session.add(tweetauston3)
    DB.session.add(tweetelon1)
    DB.session.add(tweetelon2)
    DB.session.add(tweetelon3)
    DB.session.commit()
