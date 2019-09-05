from flask import Flask, render_template, request, redirect
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

# NOTE: Follow the below for chart js and templates
# https://gitlab.com/patkennedy79/flask_chartjs_example/tree/master
@app.route('/get_data', methods=['GET', 'POST'])
def start_streaming():
    """ Stream tweets containing user defined hashtags and store them in a CSV file """
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    # Histogram of emotion classifications NOTE: currently just an array
    emotion_histogram = apply_ml(hashtag)


    # List of frequencies from the histogram
    frequencies = list(emotion_histogram.values())

    print("Histogram: {} \n Length: {}".format(frequencies, len(frequencies)))

    test_values = [30, 10, 40, 20, 20, 50]
    # return str(values)
    return render_template('display_chart.html', user_data=frequencies)
    # return str(emotion_histogram)
    # return render_template('display_chart.html')





if __name__ == "__main__":
    app.run(debug=True, port=5000)
