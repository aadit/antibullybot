


import random
import math

from time import time

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits


import numpy as np;
from numpy import genfromtxt

import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import sklearn as sk
import random
from sklearn.metrics.pairwise import cosine_similarity
from ABClassifier.clustering.SVM import SVM





def transform(unlabeled_cv_list):
	print len(unlabeled_cv_list)
	Matrix = [[0 for x in xrange(len(unlabeled_cv_list[0]))] for x in xrange(len(unlabeled_cv_list))]
	i = 0
	j = 0
	for i in range(len(unlabeled_cv_list)):
		j=0
		for j in range (len(unlabeled_cv_list[i])):	
			Matrix[i][j] = unlabeled_cv_list[i][j]
			
#		column = column + 1
#		if column == len(unlabeled_cv_list[0]):
#			row = row + 1
#			column = 0    
	return Matrix


def ttttt(unl):
	abcdef = []
	for u in unl:
		abcdef.append(u["cv"])
	return transform(abcdef)
	
def perform_clustering(unlabeled_cv_list, Matrix ,c):
	
	print len(Matrix)
	classes = [
	1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		1,1,1,1,1,1,1,1,1,1,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0
		]
	o = SVM()
#	print len(Matrix)
	o.generate_model(unlabeled_cv_list, c)
		
	
		
	classifiedLabels = o.predict(Matrix)
	return classifiedLabels;



save_location = 'E:/'
limit_1 = 100
limit_2 = 100

k_list = [100]

for k in k_list:

	print "Running experiment for k = " + str(k)
	ab = ABClassifier()
	ab.download_cursors(limit_unlabeled = limit_1, limit_labeled = limit_1)
	ab.run_lsa(k=k)

	print "Starting classification..."

	unlabeled_cursor   = ab.unlabeled_collection.find(timeout=False).limit(limit_1).skip(limit_1)
	pos_cursor = ab.labeled_collection.find({"bully":True},timeout=False).limit(limit_2)
	neg_cursor = ab.labeled_collection.find({"bully":False},timeout=False).limit(limit_2)

	unl = []
	pos = []
	neg = []

	for u,p,n in zip(unlabeled_cursor, pos_cursor, neg_cursor):

		u_obj = {}
		p_obj = {}
		n_obj = {}

		u_obj["text"] = u["text"]
		u_obj["cv"]   = ab.get_context_vector(u_obj["text"])
		unl.append(u_obj)

		p_obj["text"] = p["text"]
		p_obj["cv"]   = ab.get_context_vector(p_obj["text"])
		pos.append(p_obj)
		
		n_obj["text"] = n["text"]
		n_obj["cv"]   = ab.get_context_vector(n_obj["text"])
		neg.append(n_obj)
		

	aaa = []
	poslen = len(pos)
	
	neglen = len(neg)
	
	for negl in range(len(neg)):
		pos.append(neg[negl])
	
	aaa = ttttt(pos)
		
	classes = []
	m = 0
	n = 0
	for m in range(poslen):
		classes.append(1);
	n = poslen
	for n in range(poslen,len(pos)):
		classes.append(0);
	positive_set = []
	negative_set = []

	xyz = ttttt(unl);
	print len(xyz)
	abc =  perform_clustering(aaa, xyz, classes)
	print abc
	
	
	for y in range(len(abc)):
		if abc[y] > 0:
			x = y
			#print unl[y]["text"].encode('utf-8')
	
#	for u in unl:
	
	

	
#		if pos_similarity > neg_similarity:
#			positive_set.append(u["text"])
#
#		else:
#			negative_set.append(u["text"])

#	positive_file = open(save_location + "/positive_set_" + str(k) + ".txt", 'wb')
#	negative_file = open(save_location + "/negative_set_" + str(k) + ".txt", 'wb')


#	for p in positive_set:
#		print >> positive_file, p.encode('utf-8')

#	for n in negative_set:
#		print >> negative_file, n.encode('utf-8')

#	positive_file.close()
#	negative_file.close()

#	"Done. Files saved at " + save_location
