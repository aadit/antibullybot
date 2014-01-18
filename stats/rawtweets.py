from pymongo import MongoClient

c = MongoClient()
db = c.antibullybot
raw_tweets = db.raw_tweets

print "Total Tweets in DB: "
print raw_tweets.count()

print

print "Total Classified Tweets: "
print raw_tweets.find({"bully":{'exists':True}}).count()

print

print "Tweets Marksed as Bully: "
print raw_tweets.find({"bully": 1}).count()

print

print "Tweets Marksed as Not Bully: "
print raw_tweets.find({"bully": 0}).count()