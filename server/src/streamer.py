from twython import TwythonStreamer
from AntiBullyStreamer import AntiBullyStreamer 

#Load APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET from twitter_credentials.secret
#Note: twiter_credentials.secret will contain keys and tokens for the @AntiBullyBot account and 
#should not be pushed onto public git repository. 

s = open('twitter_credentials.secret','r')
secrets = s.read().splitlines()
s.close()

APP_KEY = secrets[0] 
APP_SECRET = secrets[1]
OAUTH_TOKEN = secrets[2]
OAUTH_TOKEN_SECRET = secrets[3]

#Get list of terms for twitter to push to our server from tracklist.txt.
#Twitter doesn't support regex search, so optimizing tracklist.txt for finding relevant
#tweets might be necessary. 
f = open('tracklist.txt','r')
tracklist = ""

#comma separate the list of terms for twitter to push to our server
for line in f:
	tracklist += line + ", " 

f.close()

stream = AntiBullyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.db_connect()
stream.statuses.filter(track = tracklist)