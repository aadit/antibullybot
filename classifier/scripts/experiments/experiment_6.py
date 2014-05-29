"""
   Experiment 6: Measuring accuracy using pre-labelled positive and negative tweets
    -Positive Examples, Negative Examples
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


def defineContextVectorMatrix(model):
	cvMatrix = []
	for u in model:
		cvMatrix.append(u["cv"])
	return transform(cvMatrix)
	
def perform_clustering(modelData, testData ,classes):
	o = SVM()
	o.generate_model(modelData, classes)
	classifiedLabels = o.predict(testData)
	return classifiedLabels;

def calaccuracy(predictedClasses,ActualClasses):
	count = 0;
	x = 0;
	for x in range(len(ActualClasses)):
		if(predictedClasses[x] == ActualClasses[x]):
			count = count + 1
	acc = float(count)/float(len(ActualClasses)) 
	acc = acc * 100
	return acc


save_location = '../../experiment_data/experiment_6'

limit_2 = 400

k_list = [100]

for k in k_list:
	print "Running experiment for k = " + str(k)
	ab = ABClassifier()
	ab.download_cursors(limit_unlabeled = limit_2, limit_labeled = limit_2)
	ab.run_lsa(k=k)

	print "Starting classification..."

	pos_cursor = ab.labeled_collection.find({"bully":True},timeout=False).limit(limit_2)
	neg_cursor = ab.labeled_collection.find({"bully":False},timeout=False).limit(limit_2)

	pos = []
	neg = []

	for p,n in zip(pos_cursor, neg_cursor):

		p_obj = {}
		n_obj = {}

		p_obj["text"] = p["text"]
		p_obj["cv"]   = ab.get_context_vector(p_obj["text"])
		pos.append(p_obj)
		
		n_obj["text"] = n["text"]
		n_obj["cv"]   = ab.get_context_vector(n_obj["text"])
		neg.append(n_obj)
		


	
	poslen = len(pos)
	
	neglen = len(neg)
	
	classes = []
	m = 0
	n = 0
	for m in range(len(neg)-100):
		classes.append(0);
	n = 0
	for n in range(0,poslen-120):
		classes.append(1);	
	model = []
	for negl in range(len(neg)-100):
		model.append(neg[negl])
	for posl in range(len(pos)-120):
		model.append(pos[posl])
	
	model = defineContextVectorMatrix(model)
		
	
	testData = []
	actualClasses = []
	m = limit_2 - 120
	n = limit_2 - 100
	for m in range(poslen-120,poslen):
		testData.append(pos[m])
		actualClasses.append(1);
	for n in range(neglen-100,neglen):
		testData.append(neg[n])
		actualClasses.append(0);
	
	testDataModel = defineContextVectorMatrix(testData);
	clusteredData =  perform_clustering(model, testDataModel, classes)
	
	print "Accuracy: " , calaccuracy(classes, actualClasses);
	
	
	positive_file = open(save_location + "/positive_set_" + str(k) + ".txt", 'wb')
	negative_file = open(save_location + "/negative_set_" + str(k) + ".txt", 'wb')
	
	for y in range(len(clusteredData)):
		if clusteredData[y] > 0:
			print >> positive_file, testData[y]["text"].encode('utf-8')
		else:
			print >> negative_file, testData[y]["text"].encode('utf-8')
	
	positive_file.close()
	negative_file.close()

	print "Done. Files saved at " + save_location



