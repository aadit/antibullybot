"""
   Experiment 4: Classify unlabelled tweets as bullying or nonbullying using SVM
    -Positive Examples, Negative Examples, Unlabeled
"""



import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
from numpy import genfromtxt
import sklearn as sk
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
import random
from sklearn.metrics.pairwise import cosine_similarity
from clustering.SVM import SVM



def transform(contextVectorList):
	Matrix = [[0 for x in xrange(len(contextVectorList[0]))] for x in xrange(len(contextVectorList))]
	i = 0
	j = 0
	for i in range(len(contextVectorList)):
		j=0
		for j in range (len(contextVectorList[i])):	
			Matrix[i][j] = contextVectorList[i][j]
			
  	return Matrix


def defineContextVectorMatrix(unl):
	cvMatrix = []
	for u in unl:
		cvMatrix.append(u["cv"])
	return transform(cvMatrix)
	
def perform_clustering(modelData, testData ,classes):
	o = SVM()
	o.generate_model(modelData, classes)
	classifiedLabels = o.predict(testData)
	return classifiedLabels;



save_location = '../../experiment_data/experiment_4'
limit_1 = 300
limit_2 = 300

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
		

	model = neg
	
	poslen = len(pos)
	
	neglen = len(neg)
	
	classes = []
	m = 0
	n = 0
	for m in range(len(model)):
		classes.append(0);
	n = 0
	for n in range(0,poslen-20):
		classes.append(1);	
	for posl in range(len(pos)-20):
		model.append(pos[posl])
	
	model = defineContextVectorMatrix(model)
		
	testData = defineContextVectorMatrix(unl);
	clusteredData =  perform_clustering(model, testData, classes)
	print clusteredData
	
	positive_file = open(save_location + "/positive_set_" + str(k) + ".txt", 'wb')
	negative_file = open(save_location + "/negative_set_" + str(k) + ".txt", 'wb')
	
	for y in range(len(clusteredData)):
		if clusteredData[y] > 0:
			print >> positive_file, unl[y]["text"].encode('utf-8')
		else:
			print >> negative_file, unl[y]["text"].encode('utf-8')
	
	positive_file.close()
	negative_file.close()

	print "Done. Files saved at " + save_location



