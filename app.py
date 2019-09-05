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


# DEBUG NOTE: In order to render chart with dynamic data:
# Put the chart JS inside the html inside a script tag
# Create a function that does an Axios request to server to retrieve data and labels and then render the chart with that data
# This means I may have to refactor my main app file to
# Use window.onload event listener in order to immediately send request when the chart page loads.
# We may want to do a set timeout request in order to allow the API to return the necessary data to render the chart




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

    labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
    values = frequencies

    # Confirming equal lengths
    print("Labels and Length: {}:{}".format(labels,len(labels)))
    print("Frequencies and Frequency Length: {}:{}".format(values,len(values)))

    return render_template('display_chart.html', values=values, labels=labels)
    # return str(emotion_histogram)
    # return render_template('display_chart.html')





if __name__ == "__main__":
    app.run(debug=True, port=5000)
