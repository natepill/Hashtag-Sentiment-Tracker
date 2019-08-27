from flask import Flask, render_template, request
from applied_ml import *
import requests
import time


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

    # Histogram of emotion classifications
    emotion_histogram = apply_ml(hashtag)

    # NOTE: Currently throwing Tensorflow error when refreshing server after rendering html
    # NOTE: Try making internal post request to a different route which renders the chart and
    # also send along the emotion_histogram
    return emotion_histogram
    # return render_template('display_chart.html')

if __name__ == "__main__":
    app.run(debug=True, port=33507)
