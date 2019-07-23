from flask import Flask, render_template, request
from stream_listener import StreamListener

import requests
import time
import tweepy
import env #Custom env file for tweepy keys
import csv

app = Flask(__name__)


@app.route('/')
def landing_page():
    # NOTE: CSS linkage is using absolute path, may cause issue during deployment
    return render_template('index.html')

@app.route('/get_data')
def start_streaming():
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

    # NOTE: builtins.UnboundLocalError, UnboundLocalError: local variable 'coords' referenced before assignment
    stream.filter(track=track_terms) # Start streaming tweets


    return hashtag

if __name__ == "__main__":
    app.run(debug=True, port=33507)
