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
		
		self.connection = MongoClient('aaditpatel.com')
		self.db = self.connection[database_name]
		self.db.authenticate(username, password)
		self.unlabeled_collection = self.db[unlabeled_data]
		self.labeled_collection = self.db[labeled_data]


	def get_cursors(self, limit_unlabeled = 100, limit_labeled = 100):
		self.unlabeled_cursor = self.unlabeled_collection.find().limit(limit_unlabeled)
		self.labeled_cursor = self.labeled_collection.find().limit(limit_labeled)

		for i in self.unlabeled_cursor:
			print i["text"]

		for i in self.labeled_cursor:
			print i["text"]



	def run_lsa(self):

		#iterates over unlabeled cursor
		#iterates over laeled cursor
			#performs nltk
			#adds into co occurrence

		#comatrix.do_svd()
		#
		pass

	def compute_context_vectors(self):
		pass







