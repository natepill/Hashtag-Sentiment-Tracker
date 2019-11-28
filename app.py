from flask import Flask, render_template, request, redirect, url_for
from __future__ import unicode_literals
from applied_ml import *
import requests
import requests
import time
import os
import json


app = Flask(__name__)


@app.route('/')
def landing_page():
    """ Return index page to prompt user for hashtags """
    # NOTE: CSS linkage is using absolute path, may cause issue during deployment
    return render_template('index.html')





@app.route('/get_data', methods=['GET', 'POST'])
def stream_data():
    """ Stream tweets containing user defined hashtags and store them in a CSV file """
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")

    # Histogram of emotion classifications
    emotion_histogram = apply_ml(hashtag)

    # String of frequencies from the histogram so we can pass to route
    # values = ''.join(list(emotion_histogram.values()))

    # 13 Emotion classes
    labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']


    # List of frequencies from the histogram
    values = list(emotion_histogram.values())

    # Store data on server to call for from client side
    store_data = {'labels':labels, 'frequencies': values}

    print(f'store_data: {store_data}')


    return render_template('display_chart.html', labels=labels, values=values, hashtag=hashtag)









# DEBUG NOTE: In order to render chart with user data:
#NOTE: The reason why I can't simply pass values via Flask's render_template is because
# Im not trying to pass values to an html template. I'm trying to utilize values in the JS file
# which cannot have values passed in.

# Put the chart JS inside the html inside a script tag
# Create a function that does an Axios request to server to retrieve data and labels and then render the chart with that data
# This means I may have to refactor my main app file to
# Use window.onload event listener in order to immediately send request when the chart page loads.
# We may want to do Async Await the Axios request in order to first get the data to render
# to set timeout request in order to allow the API to return the necessary data
# to render the chart

#
# @app.route('/get_data', methods=['GET', 'POST'])
# def stream_data():
#     """ Stream tweets containing user defined hashtags and store them in a CSV file """
#     # Grab user input from url parameter and remove whitespace
#     hashtag = request.args.get('hashtag').replace(" ", "")
#
#     # Histogram of emotion classifications
#     emotion_histogram = apply_ml(hashtag)
#
#     # String of frequencies from the histogram so we can pass to route
#     # values = ''.join(list(emotion_histogram.values()))
#
#     # 13 Emotion classes
#     labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
#
#
#     # List of frequencies from the histogram
#     values = list(emotion_histogram.values())
#
#     # Store data on server to call for from client side
#     store_data = {'labels':labels, 'frequencies': values}
#
#     print(f'store_data: {store_data}')
#
#     curr_time = time.time()
#     results_file_path = f'predicted_results/{hashtag}_{curr_time}.json'
#
#     with open(results_file_path, 'w') as file:
#         json.dump(store_data, file)
#
#     # TODO: Quickly try:
#     # Follow the below for chart js and templates
#     # https://gitlab.com/patkennedy79/flask_chartjs_example/tree/master
#
#     # Render empty chart page
#     # TODO: Note add some note, or loading JS animation to the client side as we await
#     # for the return call from the server to return the data to populate our chart JS
#     # visualization
#
#
#     # TODO Need to store hashtag and current time inside hidden tags, extract that w/ JS, and await a request
#     # Rendering the template with the necessary components to retrieve the logged form
#     return render_template('display_chart.html', hashtag=hashtag, curr_time=curr_time)




@app.route('/get_classifications', methods=['GET', 'POST'])
def get_emotion_classifications():

    # object = request.args.get('body')
    print(request.args)
    # print(object)
    # hashtag, curr_time = request.args.get('hashtag').replace(" ", "")
    print("GET classifications")

    # TODO: Need to add string substitution for correct path
    classifications_json = open('predicted_results.json', 'r')

    json_decoded = json.load(classifications_json)


    classifications_json.close()

    return json_decoded







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

    # return render_template()



# NOTE: DEPRECIATED ROUTE
# NOTE: Follow the below for chart js and templates
# https://gitlab.com/patkennedy79/flask_chartjs_example/tree/master
# @app.route('/display_chart/<values>')
# def display_chart(values):
#     """ Displays pie chart visualization of emtion classifications """
#
#     # Confirming equal lengths
#     print("Labels and Length: {}:{}".format(labels,len(labels)))
#     print("Frequencies and Frequency Length: {}:{}".format(values,len(values)))
#
#     # 13 Emotion classes
#     labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
#
#
#
#     # Load empty chart visualization
#     return render_template()






if __name__ == "__main__":
    app.run(debug=True, port=5000)
