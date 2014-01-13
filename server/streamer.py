from twython import TwythonStreamer
from AntiBullyStreamer import AntiBullyStreamer 

APP_KEY = "BjGHwZOKOrNYWXyaj3dBg"
APP_SECRET = "26sZrjNVwG9aypd2HqxUvy2yaCqFoDLGkedJrzFQ8"
OAUTH_TOKEN = "542734581-nmvfSkR2PJfKEm1XE3SAqwn3kQ19lreSNvb6GyhD"
OAUTH_TOKEN_SECRET = "3aiNEiW1BrYPjFeqJov9EVgZr0bmqxvXnjNybFhQ8Vx1g"


#Get list of 
f = open('tracklist.txt','r')
tracklist = ""

for line in f:
	tracklist += line + "," 

f.close()

stream = AntiBullyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.db_connect()
stream.statuses.filter(track = tracklist)