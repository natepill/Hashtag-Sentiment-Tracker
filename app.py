from flask import Flask, render_template, request
from stream_listener import StreamListener
from text_preprocessing import *
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import requests
import time
import pickle
import tweepy
import env #Custom env file for tweepy keys
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def landing_page():
    """ Return index page to prompt user for hashtags """
    # NOTE: CSS linkage is using absolute path, may cause issue during deployment
    return render_template('index.html')

@app.route('/get_data')
def start_streaming():
    """ Stream tweets containing user defined hashtags and store them in a CSV file """
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    # Tweepy API Authentication
    auth = tweepy.OAuthHandler(env.TWITTER_APP_KEY, env.TWITTER_APP_SECRET)
    auth.set_access_token(env.TWITTER_KEY, env.TWITTER_SECRET)
    api = tweepy.API(auth)

    # Init Tweepy Stream Listener
    twitter_stream_listener = StreamListener(hashtag)

    # List of hashtags to track, currently testing with single hashtag
    track_terms = [hashtag]

    # We pass in our stream_listener so that our callback functions are called
    stream = tweepy.Stream(auth=api.auth, listener=twitter_stream_listener)

    # Start streaming tweets
    stream.filter(track=track_terms)

    # Create pandas dataframe
    data = pd.read_csv('collected_tweets/{}'.format(twitter_stream_listener.filename))

    # Apply text cleaning to the tweet data
    data["tweet_content"] = data["tweet_content"].apply(lambda x: " ".join(normalize(x)))

    # Split each tweet into array of words
    data["tweet_content"] = data.apply(lambda row: word_tokenize(row['tweet_content']), axis=1)

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
    model = load_model('emotion_classification.h5')

    emotion_dict = {0: 'anger', 1: 'boredom',2: 'empty',3: 'enthusiasm',4: 'fun',5: 'happiness',6: 'hate',7: 'love',8: 'neutral',9: 'relief',10: 'sadness',11: 'surprise',12: 'worry'}

    # Prediction on streamed data
    y_pred = model.predict(tokenized_tweets)

    # Storing the actual classified emotions based on model results
    classified_emotions = []

    # Classify emotion based on highest probability of sentiment
    for sentiment in y_pred:
        # highest probability for output class
        max_val = np.where(sentiment == np.amax(sentiment))
        # Store the resulting output class string
        classified_emotions.append(emotion_dict[max_val[0][0]])

    return render_template('display_chart.html')
    # return str(classified_emotions)

if __name__ == "__main__":
    app.run(debug=True, port=33507)
