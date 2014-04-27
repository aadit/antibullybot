from pymongo import MongoClient
import argparse


#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r","--remote", help = "Remote host where the database is saved")
parser.add_argument("-c", "--collection", help= "The raw tweets collection name you'd like stats for")
args = parser.parse_args()


c = MongoClient(args.remote or 'localhost')
db = c.antibullybot
db.authenticate('antibullybot','antibully')

raw_tweets = db[args.collection or 'raw_tweets']


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