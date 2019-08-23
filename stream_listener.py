 # NOTE: Do I need these imports if they are being imported from the main app file?
import requests
import time
import tweepy
import env #Custom env file for tweepy keys
import csv


'''
Open a persistent connection to the Twitter API.
Preprocess each tweet that we receive.
Store the processed tweets into csv file
'''



#Overriding Tweepy's StreamListener class
class StreamListener(tweepy.StreamListener):
    '''Create a listener that prints the text of any tweet that comes from the Twitter API.'''

    def __init__(self, hashtag, time_limit=5):
        self.start_time = time.time()
        self.filename = '{}_{}.csv'.format(hashtag, self.start_time)
        self.limit = time_limit

        self.init_csv()
        super(StreamListener, self).__init__()

    def init_csv(self):
        ''' Initialize CSV file with headers '''

        with open("collected_tweets/{}".format(self.filename), 'w') as csv_file:
            fieldnames = ['tweet_context']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()


    def on_status(self, status):
        """ Streamed tweet passes through and is added to CSV """

        # Stop Twitter stream after initialized time limit
        if (time.time() - self.start_time) > self.limit:
            return False

        # If tweet is a retweet, then don’t process the tweet.
        if hasattr(status, 'retweeted_status'):
            return

        # NOTE: There are a lot of cool attributes of the status object to utilize in a DS project
        # maybe I come back later and store those values in a csv and do more analysis

        print(status.text)
        text = status.text

        # description = status.user.description
        # loc = status.user.location
        # coords = status.coordinates
        # name = status.user.screen_name
        # user_created = status.user.created_at
        # followers = status.user.followers_count
        # id_str = status.id_str
        # created = status.created_at
        # retweets = status.retweet_count


        #TODO: We could preprocess the tweets here by feeding each tweet as we stream them through our ML model
        # and then we can store the sentiment score along with these other features


        if coords is not None:
            coords = json.dumps(coords)
        # Other Tweet Properties: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        # Cool Doc examples:
            # includeretweet_count — the number of times a tweet has been retweeted.
            # withheld_in_countries — the tweet has been withheld in certain countries.
            # favorite_count — the number of times the tweet has been favorited by other users.


        # NOTE: important to use APPEND mode and NOT write mode so that we dont overrite existing tweets
        with open("collected_tweets/{}".format(self.filename), 'a') as csv_file:

            csv_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([text])

    # Override the on_error method of StreamListener so that we can handle errors coming from the Twitter API properly
    # The Twitter API will send a 420 status code if we're being rate limited. If this happens --> disconnect, any other error, keep going
    def on_error(self, status_code):
        if status_code == 420:
            return False
