
from twython import TwythonStreamer
from pymongo import MongoClient

class AntiBullyStreamer(TwythonStreamer):

	def db_connect(self):

		client = MongoClient()
		db = client.antibullybot
		self.raw_tweets = db.raw_tweets


	def on_success(self, data):

		tweet = {
			"name": data["user"]["name"],
			"screen_name": data["user"]["screen_name"],
			"user_id": data["user"]["id"],
			"text": data["text"],
			"tweet_id": data["id"]
		}
		t_id = self.raw_tweets.insert(data)
		#t_id = self.raw_tweets.insert(tweet)
		#print 'Count:'
		#print self.raw_tweets.count()

		#print ''
		#print 'Saved Tweet'
		#print tweet['screen_name'] + '-' + tweet['text']
		#print ''


	def on_error(self, status_code, data):
		print status_code
