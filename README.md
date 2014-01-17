AntiBullyBot
@antibullybot

The aim of antibullybot is the patrol Twitter for cyberbullying tweets. Antibullybot hopes to make aware the issues of cyberbullying to cyberbullies on Twitter and elsewhere. 

Components:
server -> uses the Twitter Streaming API to search for tweets matching criteria in server/src/tracklist.txt

You can run your own instance of AntiBullyBot, using your own Twitter handle. You will need to provide your own API credentials in server/src/twitter_credentials.secret. This file should contain, line separate,
API_KEY
APP_SECRET
OAUTH_TOKEN
OAUTH_TOKEN_SECRET

For more information on creating a Twitter application, please visit http://dev.twitter.com. For documentation on the Public Streaming API that AntiBullyBot uses, please visit http://dev.twitter.com/docs/streaming-apis/streams/public
