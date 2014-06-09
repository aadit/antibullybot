"""
   Experiment 13: Example Tweet Similarity:
   -Compute SVDs
   -SVM Classification using only Twitter Data
"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import svm
import sklearn
from sklearn.cluster import KMeans


save_location = '../../experiment_data/experiment_13'

k_list = [25, 50, 75, 100, 150, 200, 250, 300]


# results -> k -> kernal
results = []

limit_1 = 400 #training set
limit_2 = 400 #validation set


for k in k_list:
	print "Running experiment for k=" + str(k) + "..."
	ab = ABClassifier()
	#ab.download_cursors(limit_unlabeled = 10000, limit_labeled = 10000)
	ab.download_tweet_cursors(limit_unlabeled = 5000, limit_labeled = 5000)
	ab.run_lsa(k=k)

	pos_cursor_training = ab.labeled_collection.find({"bullying_label":"1"},timeout=False).limit(500)
	neg_cursor_training = ab.labeled_collection.find({"bullying_label":"0"},timeout=False).limit(500)

	#pos_cursor_training = ab.labeled_collection.find({"bully":True},timeout=False).limit(400)
	#neg_cursor_training = ab.labeled_collection.find({"bully":False},timeout=False).limit(400)

	pos_size = 0
	neg_size = 0
	training = []
	tlabels = []

	pos_validation = []
	pos_vlabels = []
	neg_validation = []
	neg_vlabels = []


	for p in pos_cursor_training:
		cv = ab.get_context_vector(p["text"])
		training.append(cv/np.linalg.norm(cv))
		tlabels.append(1)
		pos_size = pos_size + 1

	for n in neg_cursor_training:
		cv = ab.get_context_vector(n["text"])
		training.append(cv/np.linalg.norm(cv))
		tlabels.append(-1)
		neg_size = neg_size + 1


	kmeans = KMeans(init='k-means++', n_clusters=2, n_init=100)
	n = kmeans.fit_predict(training)

	cluster_1_pos = 0;
	cluster_2_pos = 0;
	cluster_1_neg = 0;
	cluster_2_neg = 0;

	for i in xrange(0,pos_size-1):
		if n[i] == 1:
			cluster_1_pos += 1
		else:
			cluster_2_pos += 1

	for i in xrange(pos_size, neg_size + pos_size - 1):
		if n[i] == 1:
			cluster_1_neg += 1

		else:
			cluster_2_neg += 1

	cluster_1_pos_rate = float(cluster_1_pos)/(cluster_1_pos + cluster_1_neg)
	cluster_2_pos_rate = float(cluster_2_pos)/(cluster_2_pos + cluster_2_neg)

	print cluster_1_pos_rate
	print cluster_2_pos_rate

"""
	for p in pos_cursor_validation:
		cv = ab.get_context_vector(p["text"])
		pos_validation.append(cv/np.linalg.norm(cv))
		pos_vlabels.append(1)

	for n in neg_cursor_validation:
		cv = ab.get_context_vector(n["text"])
		neg_validation.append(cv/np.linalg.norm(cv))
		neg_vlabels.append(-1)

	for kernel in kernel_list:

		scores = {}
		scores["k"] = k
		scores["kernel"] = kernel

		print "Performing SVM for " + kernel + "..."
		degree = 1
		if kernel == "poly_2":
			kernel = "poly"
			degree = 2

		if kernel == "poly_3":
			kernel = "poly"
			degree = 3

		clf = svm.SVC(kernel=kernel, degree = degree, max_iter = 5000000)
		clf.fit(training, tlabels) 

		print "Done Training..."

		print "Validating..."
		
		pos_score = clf.score(pos_validation, pos_vlabels)

		neg_score = clf.score(neg_validation, neg_vlabels)

		total_score = clf.score(pos_validation+neg_validation,pos_vlabels + neg_vlabels)

		scores["pos_score"] = pos_score
		scores["neg_score"] = neg_score
		scores["total_score"] = total_score

		print pos_score
		print neg_score
		print total_score

		results.append(scores)

for r in results:
	print "k: " + str(r["k"])
	print "kernel: " + str(r["kernel"])
	print "pos_score: " + str(r["pos_score"])
	print "neg_score: " + str(r["neg_score"])
	print "total_score: " + str(r["total_score"])

import csv
with open(save_location +'/scores.csv', 'wb') as f:
	keys = ["k", "kernel", "pos_score", "neg_score", "total_score"]
	writer = csv.DictWriter(f,keys)
	writer.writerows(results)
"""


