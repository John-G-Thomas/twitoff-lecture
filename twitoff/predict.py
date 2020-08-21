"""Prediction of Users based on Tweet embeddings."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


# from .visaliztion import plot_confusion_matrix


# import SentimentIntensityAnalyzer class
# from vaderSentiment.vaderSentiment module.
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# function to print sentiments
# of the sentence.
# def sentiment_scores(sentence):
# Create a SentimentIntensityAnalyzer object.
# sid_obj = SentimentIntensityAnalyzer()

# polarity_scores method of SentimentIntensityAnalyzer
# object gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
# sentiment_dict = sid_obj.polarity_scores(sentence)

# print("Overall sentiment dictionary is : ", sentiment_dict)
# print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
# print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
# print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

# print("Sentence Overall Rated As", end=" ")

# decide sentiment as positive, negative and neutral
# if sentiment_dict['compound'] >= 0.05:
# print("Positive")

# elif sentiment_dict['compound'] <= - 0.05:
# print("Negative")

# else:
# print("Neutral")


def predict_user(user1_name, user2_name, tweet_text):
    """
    Determine and return which is more likely to say a given tweet.

    Example execution: predict_user('austen', 'elonmusk', 'Lambda School rocks!)'
    Return 1 (corresponding to first user passed in) or 0 (second).
    """
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression(max_iter=1000).fit(embeddings, labels)
    # We've done our data science! now to predict
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))  # sentiment_scores(tweet_text)


"""
Evaluate model and visalization
"""

# def Evaluate_Model():
# Users = User.query.filter(User.name)
# tweet__embeddings = np.array([tweet.embedding for tweet in Users.tweets])
# names = User.name
# return plot_confusion_matrix(cm=tweet__embeddings,
# target_names=names,
# title='Evaluation of Logistic Regression model',
# cmap=None,
# normalize=True)
