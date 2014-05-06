# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
import sys
sys.path.append('..')
import numpy as np
import itertools
import string
from scipy import linalg
from lsa.Parsing import CoMatrix
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords

# <codecell>

#Run this once to download stopwords corpus. 
#nltk.download()

# <codecell>

c = MongoClient('aaditpatel.com')
db = c.antibullybot
db.authenticate('antibullybot', 'antibully')
raw_tweets = db['raw_tweets']

# <codecell>

LIMIT=300
all_raw_tweets = raw_tweets.find(limit=LIMIT)

# <codecell>

m = CoMatrix()
m.reset()

# <codecell>

def tr_word(word) :
    ''' Returns word in which the only allowed punctuations are apostrophe and # at the beginning. Removes #. '''
    #remove leading hashtag if it exists
    word = word.lstrip('#')
    ret_word = ''
    for ch in word :
        if ch in string.ascii_lowercase or ch == '\'' :
            ret_word += ch
        else : return None
    return ret_word

# <codecell>

def ch_range(word) :
    for ch in word :
        if ord(ch) >= 128 :
            return False
    return True

# <codecell>

def build_from_data(m, db_cursor) :
	''' Updates co-occurrence matrix *m* by adding in tweets from *db_cursor*. '''

	''' Keep *st_words* as a class variable. '''
	st_words = set(stopwords.words('english'))
	st_words.add('rt')
	for rec in db_cursor:
		tweet = rec['text']
		# get individual words from the tweet. Here, a word is anything demarcated by whitespace (in particular, contains puncts)
    		tweet_tokens = nltk.regexp_tokenize(tweet, r'\S+')
		
		# Check the range, and convert to lowercase. Range checking for ruling out unicode chars.
		tweet_tokens= set([tr_word(str(string.lower(tkn))) for tkn in tweet_tokens if ch_range(tkn)])

		# Check for stop-words.
    		tweet_tokens = [word for word in tweet_tokens if word is not None and word not in st_words]

		# Update matrix.
		m.add(tweet_tokens)


