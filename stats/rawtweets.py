from pymongo import MongoClient

c = MongoClient()
db = c.antibullybot
raw_tweets = db.raw_tweets

bully_tweets = raw_tweets.find({"bully": "1"})
nonbully_tweets = raw_tweets.find({"bully": "0"})
unclassified_tweets = raw_tweets.find({"bully": {"$exists": False}})


print "Total Tweets in DB: "
print raw_tweets.count()

print

print "Total Classified Tweets: "
print raw_tweets.find({"bully":{'$exists':True}}).count()

print

print "Tweets Marked as Bully: "
print bully_tweets.count()

print

print "Tweets Marked as Not Bully: "
print nonbully_tweets.count()