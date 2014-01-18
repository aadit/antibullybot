from pymongo import MongoClient

c = MongoClient()
db = c.antibullybot
raw_tweets = db.raw_tweets

print "Total Tweets in DB: " + raw_tweets.count()

print "Total Classified Tweets: " + raw_tweets.find({"bully":{'exists':True}}).count()

print "Tweets Marksed as Bully: " + raw_tweets.find({"bully": 1}).count()

print "Tweets Marksed as Not Bully: " + raw_tweets.find({"bully": 0}).count()