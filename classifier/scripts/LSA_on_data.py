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

# <codecell>

c = MongoClient('aaditpatel.com')
db = c.antibullybot
db.authenticate('antibullybot', 'antibully')
raw_tweets = db['raw_tweets']

# <codecell>

LIMIT=3
all_raw_tweets = raw_tweets.find(limit=LIMIT)

# <codecell>

m = CoMatrix()
m.reset()

# <codecell>

def tr_word(word) :
    ''' Returns word in which the only allowed punctuations are apostrophe and #. Removes #. '''
    ret_word = ''
    for ch in word :
        if ch in string.ascii_lowercase or ch == '\'' :
            ret_word += ch
        elif ch == '#' :
            pass    
        else : return None
    return ret_word        

# <codecell>

def ch_range(word) :
    for ch in word :
        if ord(ch) >= 128 :
            return False
    return True

# <codecell>

for rec in all_raw_tweets :
    tweet = rec['text']
    tweet_tokens = nltk.regexp_tokenize(tweet, r'\S+')
    #print tweet_tokens
    tweet_tokens= set([str(string.lower(tkn)) for tkn in tweet_tokens if ch_range(tkn)])
    tweet_tokens = [tr_word(word) for word in tweet_tokens if tr_word(word) is not None]
    m.add(tweet_tokens)
    print tweet
    print tweet_tokens

# <codecell>

m.comat.shape

# <codecell>

m.do_svd(50)

# <codecell>

# -- clustering -- #

