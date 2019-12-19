# Hashtag Emotion Chart Visualization

{INSERT IMAGE}

Ever wanted to get an overall feel of how a trending hashtag is doing on Twitter? Or maybe track how people are reacting to the hashtag of your marketing campaign? Just visit {INSERT LIVE LINK} and enter the hashtag that you want to track the emotion of. It may take a 5-10 seconds to gather the tweets, but you will soon be presented with a pie chart visualization behind the emotions of what people are feeling behind that hashtag.

## How it works
Using Tweepy, Twitter's data streaming API, in order to obtain the tweets that utilize the hashtag given by the user. All collected tweets are then saved to a CSV file and are sent to be preprocessed. Once preprocessed, the tweets are run through a neural network MLP classifier with a word embedding layer into 13 possible labels (emotions):
* Anger
* Boredom
* Empty
* Enthusiasm
* Fun
* Happiness
* Hate
* Love
* Neutral
* Relief
* Sadness
* Surprise
* Worry



### Installing and Usage

To utilize this application, visit: {INSERT LIVE LINK} and enter the hashtag you wish to track the emotion behind.

For local usage run the following commands:
* git clone https://github.com/natepill/Hashtag-Sentiment-Tracker.git
* cd Hashtag-Sentiment-Tracker
* pip install -r requirements.txt
* python app.py


## Next Steps
* Given multiple hashtags to track, not just a single one
* Add user accounts so users may save and reference back to prior tracking sessions
* Give users dashboard analytics of all the metadata from the people using the hashtag they entered provided by the Tweepy API.


## Built With
* Tweepy API
* ChartJS
* Keras
* Sklearn
* nltk

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License
