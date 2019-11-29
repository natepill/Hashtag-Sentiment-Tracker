from __future__ import unicode_literals
from stream_listener import StreamListener
from text_preprocessing import *
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

import pickle
import tweepy
import csv
import pandas as pd
import numpy as np
import tensorflow as tf

import os


# Start TF graph session
graph = tf.get_default_graph()


model = load_model('emotion_classification.h5')


def start_stream(hashtag):
    """
        Stream data through Tweepy API with given hashtag and
        return resulting CSV filename
    """

    # Tweepy API Authentication
    auth = tweepy.OAuthHandler(os.environ["TWITTER_APP_KEY"], os.environ["TWITTER_APP_SECRET"])
    auth.set_access_token(os.environ["TWITTER_KEY"], os.environ["TWITTER_SECRET"])
    api = tweepy.API(auth)

    # Init Tweepy Stream Listener
    twitter_stream_listener = StreamListener(hashtag)

    # List of hashtags to track, currently testing with single hashtag
    track_terms = [hashtag]

    # We pass in our stream_listener so that our callback functions are called
    stream = tweepy.Stream(auth=api.auth, listener=twitter_stream_listener)

    # Start streaming tweets
    stream.filter(track=track_terms)


    return twitter_stream_listener.filename


def clean_data(filename):
    """ Normalize text data and return in pandas dataframe """
    # Create pandas dataframe
    data = pd.read_csv('collected_tweets/{}'.format(filename))

    # Apply text cleaning to the tweet data
    data["tweet_content"] = data["tweet_content"].apply(lambda x: " ".join(normalize(x)))

    # Split each tweet into array of words
    data["tweet_content"] = data.apply(lambda row: word_tokenize(row['tweet_content']), axis=1)

    return data


def emotion_classification(data):
    """ Apply ML model for classification and return histogram of output classes """
    # Unpickling the trained tokenizer to one hot encode our tweets
    pickled_file = open('trained_tokenizer.pickle', 'rb')
    keras_tokenizer = pickle.load(pickled_file)
    pickled_file.close()

    # One hot encode tweets using trained keras tokenizer
    tokenized_tweets = keras_tokenizer.texts_to_sequences(data["tweet_content"])

    # Pad sequences to accomadate 100 unique vocab
    max_len = 100
    tokenized_tweets = pad_sequences(tokenized_tweets, maxlen = max_len)

    # Loading in trained keras model for classification


    emotion_dict = {
    0: 'anger', 1: 'boredom', 2: 'empty', 3: 'enthusiasm',
    4: 'fun', 5: 'happiness', 6: 'hate', 7: 'love', 8: 'neutral',
    9: 'relief', 10: 'sadness', 11: 'surprise', 12: 'worry'
    }

    # Prediction on streamed data
    with graph.as_default():
        y_pred = model.predict(tokenized_tweets)

    # Storing the actual classified emotions based on model results
    classified_emotions = {
    'anger': 0, 'boredom': 0, 'empty': 0, 'enthusiasm': 0,
    'fun': 0, 'happiness': 0, 'hate': 0, 'love': 0,
    'neutral': 0, 'relief': 0, 'sadness': 0, 'surprise': 0, 'worry':0
    }

    # print("CLASSIFIED EMOTIONS: {}".format(len(classified_emotions)))

    # Classify emotion based on highest probability of sentiment
    for sentiment in y_pred:
        # highest probability for output class
        max_val = np.where(sentiment == np.amax(sentiment))
        # Store the resulting output class string
        # NOTE may want to create histogram here
        emotion = emotion_dict[max_val[0][0]]

        # Build histogram
        if emotion in classified_emotions:
            classified_emotions[emotion] += 1
        else:
            classified_emotions[emotion] = 1



    return classified_emotions


def apply_ml(hashtag):
    """
        Main function for streaming and cleaning data as well as
        applying ml for classification
    """
    print("Hashtag:", hashtag)
    csv_filename = start_stream(hashtag)
    cleaned_data = clean_data(csv_filename)
    histogram = emotion_classification(cleaned_data)
    # print("APPLIED ML\n =========== \n  Histogram: {} \n Length: {}".format(histogram, len(histogram)))

    return histogram
