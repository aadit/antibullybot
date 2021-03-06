import sys
sys.path.append('..')
from lsa.Parsing import CoMatrix
#from classifier.kMeans import kMeans
#from classifier.SVM import SVM
import numpy as np
import itertools
import string
from scipy import linalg
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import random


#This class connects to a remote repository to fetch the labeled data and unlabeled data. 
#It also itnerfaces with the CoMatrix class to perfrom LSA, and with Clustering class to perform SVM, KMeans, etc
class ABClassifier: 


 	def __init__(self, host = "aaditpatel.com", database_name = "antibullybot", unlabeled_data = "raw_tweets_4_27_2014", labeled_data = "labeled_data", username = "antibullybot", password ="antibully"):
		
		print "Connecting to database at " + host + "..."

		#MongoDB Connection Variables
		self.connection = MongoClient(host)
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
		self.pos_labeled_cv_list = []
		self.neg_labeled_cv_list = []

		print "Connected."


	def download_cursors(self, limit_unlabeled = 100, limit_labeled = 100, batch_size = 120):
		
		print "Downloading cursors with batch size " + str(batch_size) + "..."

		self.unlabeled_cursor = self.unlabeled_collection.find(timeout=False).limit(limit_unlabeled).batch_size(batch_size)
		self.pos_labeled_cursor = self.labeled_collection.find({"bully":True},timeout=False).limit(limit_labeled).batch_size(batch_size)
		self.neg_labeled_cursor = self.labeled_collection.find({"bully":False},timeout=False).limit(limit_labeled).batch_size(batch_size)

		print "Downloaded."

	def download_tweet_cursors(self, limit_unlabeled = 100, limit_labeled = 100, batch_size = 120):
		
		print "Downloading cursors with batch size " + str(batch_size) + "..."

		self.labeled_collection = self.db["tweets"]

		skip_num = random.randrange(0,110000)

		self.unlabeled_cursor   = self.unlabeled_collection.find(timeout=False).limit(limit_unlabeled).skip(skip_num).batch_size(batch_size)
		self.pos_labeled_cursor = self.labeled_collection.find({"bullying_label":"1"},timeout=False).limit(limit_labeled).batch_size(batch_size)
		self.neg_labeled_cursor = self.labeled_collection.find({"bullying_label":"0"},timeout=False).limit(limit_labeled).batch_size(batch_size)

		print "Downloaded."



	#run lsa on unlabeled and labeled cursors
	def run_lsa(self, k=100): 

		print "Running LSA with rank approximation " + str(k) + "..."


		self.m.reset()

		print "Computing Co-Occurrence Matrix..."
		#Build co-occurrence matrix 
		self.build_cooccurrence(self.m, self.unlabeled_cursor)
		self.build_cooccurrence(self.m, self.pos_labeled_cursor)
		self.build_cooccurrence(self.m, self.neg_labeled_cursor)

		print "Computed."
		print "Starting SVD..."
		
		self.m.do_svd(k)

		#Reset cursors
		self.unlabeled_cursor.rewind()
		self.pos_labeled_cursor.rewind()
		self.neg_labeled_cursor.rewind()

		print "Finished SVD"

		return self.m


	def get_context_vector(self, text):
		tweet_tokens = self.do_nltk(text)
		return self.m.get_context_vector(tweet_tokens)


	def compute_context_vectors(self, save_location):

		print "Computing context vectors..."

		self.unlabeled_cv_list = []
		self.pos_labeled_cv_list = []
		self.neg_labeled_cv_list = []

		#do for unlabeled data
		for c in self.unlabeled_cursor:
			text = c['text']
			tweet_tokens = self.do_nltk(text)
			cv = self.m.get_context_vector(tweet_tokens)
			if np.linalg.norm(cv) == 0:
				#print text
				#print tweet_tokens
				pass

			else:
				self.unlabeled_cv_list.append(cv)

		#do for labeled data
		for c in self.pos_labeled_cursor:
			text = c['text']
			tweet_tokens = self.do_nltk(text)
			cv = self.m.get_context_vector(tweet_tokens)

			if np.linalg.norm(cv) == 0:
				pass
			else:
				self.pos_labeled_cv_list.append(cv)

		for c in self.neg_labeled_cursor:
			text = c['text']
			tweet_tokens = self.do_nltk(text)
			cv = self.m.get_context_vector(tweet_tokens)

			if np.linalg.norm(cv) == 0:
				pass
			else:
				self.neg_labeled_cv_list.append(cv)

		print "Saving context vectors at " + save_location + "..."
		
		l = np.array(self.pos_labeled_cv_list)
		m = np.array(self.neg_labeled_cv_list)
		n = np.array(self.unlabeled_cv_list)
		ll = np.asarray(l)
		mm = np.asarray(m)
		nn = np.asarray(n)
		np.savetxt(save_location + '/' + 'context_vectors_pos.csv', ll, delimiter=",")
		np.savetxt(save_location + '/' + 'context_vectors_neg.csv', mm, delimiter=",")
		np.savetxt(save_location + '/' + 'context_vectors_unl.csv', nn, delimiter=",")


		#Reset cursors
		self.unlabeled_cursor.rewind()
		self.pos_labeled_cursor.rewind()
		self.neg_labeled_cursor.rewind()


		print "Done."


	def compute_cosine_similarity(self, cv1,cv2):
		if np.linalg.norm(cv1) == 0 or np.linalg.norm(cv2) == 0 :
			return 0
		else:
			return np.inner(cv1,cv2)/(np.linalg.norm(cv1) * np.linalg.norm(cv2))


	def pairwise_similarity(self, cv_list):

		indeces = range(len(cv_list))
		keys = itertools.permutations(indeces, 2)
		dist_map = {}
		for i,j in keys :
			#dist_map[(i,j)] = self.compute_cosine_similarity(cv_list[i], cv_list[j])
			dist_map[(i,j)] = cosine_similarity(cv_list[i], cv_list[j])[0][0]

		return dist_map


	def perform_clustering(self, type = "KMeans"):
		array = self.transformInto2DArray(self.unlabeled_cv_list)
		self.n = kMeans()
		clusters = self.m.perform_Kmeans(array, 2)
        
	def perform_clustering(self, type = "SVM"):
		# classes holds labels for testing data -- to be defined
		array = self.transformInto2DArray(self.labeled_cv_list)
		self.o = SVM()
		self.o.generate_model(array, classes)
		unlabelled_data =  self.transformInto2DArray(self.unlabeled_cv_list)
		classifiedLabels = self.o.predict(unlabelled_data)


	"""PRIVATE METHODS"""

	#Returns word in which the only allowed punctuations are apostrophe and # at the beginning. Removes #. '''
	def tr_word(self,word) :
	    # strip non-ascii chars
	    ascii_word = self.strip_non_ascii(word) 
	    if len(ascii_word) == 0 : return ''
	    # if leading `@', return None
	    if ascii_word[0] == '@' : return None
	    # strip all puncts, except apostrophe
	    ret_word = ''
	    for ch in ascii_word :
	        if ch in string.ascii_lowercase or ch == '\'' :
	            ret_word += ch
	        else : pass
	    return ret_word


	def ch_range(self, word):
		for ch in word:
			if ord(ch) >= 128:
				return False
		return True

	#Updates co-occurrence matrix *m* by adding in tweets from *db_cursor*.
	def build_cooccurrence(self, m, db_cursor):
		#i = 0
		for rec in db_cursor:
			tweet = rec['text']
			tweet_tokens = self.do_nltk(tweet)
			#print i
			#i=i+1
			# Update matrix.
			m.add(tweet_tokens)

	def strip_non_ascii(self, word) : 
		ascii_word = ''
		for ch in word : 
			if ord(ch) < 128 :
				ascii_word += ch
			else : pass
		return ascii_word

	def do_nltk(self,tweet):
    	# get individual words from the tweet. Here, a word is anything demarcated by whitespace (in particular, contains puncts)
		tweet_tokens = nltk.regexp_tokenize(tweet, r'\S+')
		
		# Check the range, and convert to lowercase. Range checking for ruling out unicode chars.
		tweet_tokens= set([self.tr_word(str(string.lower(self.strip_non_ascii(tkn)))) for tkn in tweet_tokens])

		# Check for stop-words.
		tweet_tokens = [word for word in tweet_tokens if word is not None and word not in self.st_words and word is not '']

		return tweet_tokens

    # transforms Array of Lists into 2D Array for classification
	def transformInto2DArray(self, unlabeled_cv_list):
		Matrix = [[0 for x in xrange(len(unlabeled_cv_list[0]))] for x in xrange(len(unlabeled_cv_list))]
		row = 0
		column = 0
		for i in np.nditer(unlabeled_cv_list):
			Matrix[row][column] = i
			column = column + 1
			if column == len(unlabeled_cv_list[0]):
				row = row + 1
				column = 0    
 
		return Matrix




