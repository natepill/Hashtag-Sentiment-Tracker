from flask import Flask, render_template, request
import requests
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

    # Histogram of emotion classifications NOTE: currently just an array
    emotion_histogram = apply_ml(hashtag)

    # TODO: Try seperating out the visualization to a different route?
    # requests.post('http://localhost:33507/display_visualization', emotion_histogram)

    # NOTE: Currently throwing Tensorflow error when refreshing server after rendering html
    # NOTE: Try making internal post request  to a different route which renders the chart and
    # also send along the emotion_histogram
    # return str(emotion_histogram)
    return render_template('display_chart.html')

@app.route('/display_visualization', methods=['GET', 'POST'])
def display_chart():
    pass



if __name__ == "__main__":
    app.run(debug=True, port=33507)
