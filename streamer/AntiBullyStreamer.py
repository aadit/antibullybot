
from twython import TwythonStreamer
from pymongo import MongoClient

class AntiBullyStreamer(TwythonStreamer):

	def db_connect(self, table_name = "raw_tweets_2", remote = "localhost", echo_tweets = False):

		client = MongoClient(remote)
		db = client.antibullybot
		db.authenticate('antibullybot','antibully')
		self.raw_tweets = db[table_name]
		self.echo_tweets = echo_tweets


	def on_success(self, data):

		tweet = {
			"name": data["user"]["name"],
			"screen_name": data["user"]["screen_name"],
			"user_id": data["user"]["id"],
			"text": data["text"],
			"tweet_id": data["id"]
		}

		if "@" in data["text"]:

			if not data["text"].startswith("RT"):
				t_id = self.raw_tweets.insert(data)

				#t_id = self.raw_tweets.insert(tweet)
				#print 'Count:'
				#print self.raw_tweets.count()
				if self.echo_tweets:
					print ''
					print 'Saved Tweet'
					print tweet['screen_name'] + '-' + tweet['text']
					print ''


	def on_error(self, status_code, data):
		print status_code
