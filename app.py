from flask import Flask, render_template, request, redirect, url_for
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
@app.route('/display_chart/<values>')
def display_chart(values):
    """ Displays pie chart visualization of emtion classifications """

    # Confirming equal lengths
    print("Labels and Length: {}:{}".format(labels,len(labels)))
    print("Frequencies and Frequency Length: {}:{}".format(values,len(values)))

    # 13 Emotion classes
    labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']

    # Load empty chart visualization
    return render_template('display_chart.html', values=values, labels=labels)



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

@app.route('/get_data', methods=['GET', 'POST'])
def stream_data():
    """ Stream tweets containing user defined hashtags and store them in a CSV file """
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    # Histogram of emotion classifications
    emotion_histogram = apply_ml(hashtag)

    # String of frequencies from the histogram so we can pass to route
    # values = ''.join(list(emotion_histogram.values()))

    # List of frequencies from the histogram
    values = list(emotion_histogram.values())

    print(f"VALUES: {values}")

    # Pass along the computed frequencies for the emotion classes
    return url_for('display_chart', values=values)



# NOTE: Keep for reference

# @app.route('/get_data', methods=['GET'])
# def start_streaming():
#     """ Stream tweets containing user defined hashtags and store them in a CSV file """
#     # Grab user input from url parameter and remove whitespace
#     hashtag = request.args.get('hashtag').replace(" ", "")
#
#     # Histogram of emotion classifications
#     emotion_histogram = apply_ml(hashtag)
#
#
#     # List of frequencies from the histogram
#     values = list(emotion_histogram.values())
#
#     print("Histogram: {} \n Length: {}".format(values, len(values)))
#
#     # 13 Emotion classes
#     labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
#
#
#     # Confirming equal lengths
#     print("Labels and Length: {}:{}".format(labels,len(labels)))
#     print("Frequencies and Frequency Length: {}:{}".format(values,len(values)))
#
#
#     # Frequencies and labels to be used to fill Pie chart
#     return (values, labels)

    # return render_template('display_chart.html', values=values, labels=labels)






if __name__ == "__main__":
    app.run(debug=True, port=5000)
