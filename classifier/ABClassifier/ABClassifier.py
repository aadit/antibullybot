import sys
sys.path.append('..')
from lsa.Parsing import CoMatrix
import numpy as np
import itertools
import string
from scipy import linalg
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords

#This class connects to a remote repository to fetch the labeled data and unlabeled data. 
#It also itnerfaces with the CoMatrix class to perfrom LSA, and with Clustering class to perform SVM, KMeans, etc
class ABClassifier: 


 	def __init__(self, host = "aaditpatel.com", database_name = "antibullybot", unlabeled_data = "raw_tweets_4_27_2014", labeled_data = "labeled_data", username = "antibullybot", password ="antibully"):
		
		#MongoDB Connection Variables
		self.connection = MongoClient('aaditpatel.com')
		self.db = self.connection[database_name]
		self.db.authenticate(username, password)
		self.unlabeled_collection = self.db[unlabeled_data]
		self.labeled_collection = self.db[labeled_data]

		#Stop Words from NLTK
		self.st_words = set(stopwords.words('english'))
		self.st_words.add('rt')

		#CoOccurrence Matrix 
		self.m = CoMatrix()

		#Context Vectors
		self.unlabeled_cv_list = []
		self.labeled_cv_list = []


	def download_cursors(self, limit_unlabeled = 100, limit_labeled = 100):
		self.unlabeled_cursor = self.unlabeled_collection.find().limit(limit_unlabeled)
		self.labeled_cursor = self.labeled_collection.find().limit(limit_labeled)


	#run lsa on unlabeled and labeled cursors
	def run_lsa(self, k=100): 

		self.m.reset()

		#Build co-occurrence matrix 
		self.build_cooccurrence(self.m, self.unlabeled_cursor)
		self.build_cooccurrence(self.m, self.labeled_cursor)

		self.m.do_svd(k)

		#Reset cursors
		self.unlabeled_cursor.rewind()
		self.labeled_cursor.rewind()

		return self.m

	def compute_context_vectors(self):
		self.unlabeled_cv_list = []
		self.labeled_cv_list = []

		#do for unlabeled data
		for c in self.unlabeled_cursor:
			text = c['text']
			tweet_tokens = self.do_nltk(text)
			cv = self.m.get_context_vector(tweet_tokens)
			self.unlabeled_cv_list.append(cv)

		#do for labeled data
		for c in self.labeled_cursor:
			tweet = c['text']
			tweet_tokens = self.do_nltk(text)
			cv = self.m.get_context_vector(tweet_tokens)
			self.labeled_cv_list.append(cv)



	def computing_cosine_similarities(self, cv1,cv2):
		pass


	def perform_clustering(self, type = "SVM"):
		pass


	"""PRIVATE METHODS"""

	#Returns word in which the only allowed punctuations are apostrophe and # at the beginning. Removes #. '''
	def tr_word(self,word) :
	    #remove leading hashtag if it exists
	    word = word.lstrip('#')
	    ret_word = ''
	    for ch in word :
	        if ch in string.ascii_lowercase or ch == '\'' :
	            ret_word += ch
	        else : return None
	    return ret_word


	def ch_range(self, word):
		for ch in word:
			if ord(ch) >= 128:
				return False
		return True

	#Updates co-occurrence matrix *m* by adding in tweets from *db_cursor*.
	def build_cooccurrence(self, m, db_cursor):
		for rec in db_cursor:
			tweet = rec['text']
			tweet_tokens = self.do_nltk(tweet)
			# Update matrix.
			m.add(tweet_tokens)

	def do_nltk(self,tweet):
    	# get individual words from the tweet. Here, a word is anything demarcated by whitespace (in particular, contains puncts)
		tweet_tokens = nltk.regexp_tokenize(tweet, r'\S+')
		
		# Check the range, and convert to lowercase. Range checking for ruling out unicode chars.
		tweet_tokens= set([self.tr_word(str(string.lower(tkn))) for tkn in tweet_tokens if self.ch_range(tkn)])

		# Check for stop-words.
		tweet_tokens = [word for word in tweet_tokens if word is not None and word not in self.st_words]

		return tweet_tokens

	





