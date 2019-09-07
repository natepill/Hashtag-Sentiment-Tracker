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
#NOTE: The reason why I can't simply pass values via Flask's render_template is because
# Im not trying to pass values to an html template. I'm trying to utilize values in the JS file
# which cannot have values passed in. Uh DUH!

# Put the chart JS inside the html inside a script tag
# Create a function that does an Axios request to server to retrieve data and labels and then render the chart with that data
# This means I may have to refactor my main app file to
# Use window.onload event listener in order to immediately send request when the chart page loads.
# We may want to do Async Await the Axios request in order to first get the data to render
# to set timeout request in order to allow the API to return the necessary data
# to render the chart


@app.route('/get_data', methods=['GET'])
def start_streaming():
    """ Stream tweets containing user defined hashtags and store them in a CSV file """
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    # Histogram of emotion classifications
    emotion_histogram = apply_ml(hashtag)


    # List of frequencies from the histogram
    values = list(emotion_histogram.values())
    print("Histogram: {} \n Length: {}".format(frequencies, len(frequencies)))

    # 13 Emotion classes
    labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']


    # Confirming equal lengths
    print("Labels and Length: {}:{}".format(labels,len(labels)))
    print("Frequencies and Frequency Length: {}:{}".format(values,len(values)))



    return render_template('display_chart.html', values=values, labels=labels)



# NOTE: Follow the below for chart js and templates
# https://gitlab.com/patkennedy79/flask_chartjs_example/tree/master
@app.route('/display_chart', methods=['GET'])
def pie_chart():

    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    print("This is hashtag:", hashtag)
    return render_template('display_chart.html', hashtag=hashtag)






if __name__ == "__main__":
    app.run(debug=True, port=5000)
