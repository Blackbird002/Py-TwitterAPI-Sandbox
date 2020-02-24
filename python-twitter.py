import json
import os
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Get the dictionary of twitter OAth keys
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
keys_file = os.path.join(THIS_FOLDER, "twitterKeys.json")

with open(keys_file) as twitterKeyFile:
  twitterKeys = json.load(twitterKeyFile)

class TwitterStreamer():

  def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
    """
    Class for streaming and processing live tweets.
    """

    #Handles Twitter authentication and the connection to Twitter Streaming API.
    listener = StdOutTwitterListener(fetched_tweet_filename)

    #API key & API secret key goes here...
    auth = OAuthHandler(twitterKeys.get("consumer_key"),
                        twitterKeys.get("consumer_secret"))

    #API Access token & secret token
    auth.set_access_token(twitterKeys.get("access_token_key"),
                          twitterKeys.get("access_token_secret"))

    stream = Stream(auth, listener)

    # This line filter Twitter Streams to capture data by the keywords: 
    stream.filter(track=hash_tag_list)


class StdOutTwitterListener(StreamListener):
  """
  Basic testing listener class that prints received tweets to stdout.
  """
  def __init__(self, fetched_tweet_filename):
    self.fetched_tweets_filename = fetched_tweet_filename

  def on_data(self, data):
    print("Type of data is: ", type(data))
    try:
      #Deserialize string and create python object
      jsonTweets = json.loads(data)

      #Append to the file...
      with open(self.fetched_tweets_filename, "a") as f:
        json.dump(jsonTweets,f, indent=2)
    except BaseException as e:
      print("Error on_data: %s", str(e))
    return True

  def on_error(self, status):
    print(status)

if  __name__ == "__main__":
  hash_tag_list = ["String"]
  fetched_tweets_filename = "Tweets.json"
  twitterStreamer = TwitterStreamer()
  twitterStreamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
