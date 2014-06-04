"""
   Experiment 12: Example Tweet Similarity:
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



save_location = '../../experiment_data/experiment_12'

k_list = [25, 50, 75, 100, 150, 200, 250, 300]

kernel_list = ["linear", "poly", "rbf"]

# results -> k -> kernal
results = []

limit_1 = 400 #training set
limit_2 = 400 #validation set


for k in k_list:
	print "Running experiment for k=" + str(k) + "..."
	ab = ABClassifier()
	ab.download_cursors(limit_unlabeled = 10000, limit_labeled = 10000)
	#ab.download_tweet_cursors(limit_unlabeled = 800, limit_labeled = 1000)
	ab.run_lsa(k=k)

	#pos_cursor_training = ab.labeled_collection.find({"bullying_label":"1"},timeout=False).limit(400)
	#neg_cursor_training = ab.labeled_collection.find({"bullying_label":"0"},timeout=False).limit(400)

	pos_cursor_training = ab.labeled_collection.find({"bully":True},timeout=False).limit(400)
	neg_cursor_training = ab.labeled_collection.find({"bully":False},timeout=False).limit(400)

	training = []
	tlabels = []

	pos_validation = []
	pos_vlabels = []
	neg_validation = []
	neg_vlabels = []


	for p in pos_cursor_training:
		training.append(ab.get_context_vector(p["text"]))
		tlabels.append(1)

	for n in neg_cursor_training:
		training.append(ab.get_context_vector(n["text"]))
		tlabels.append(-1)


	pos_cursor_validation = ab.db["tweets"].find({"bullying_label":"1"},timeout=False)
	neg_cursor_validation = ab.db["tweets"].find({"bullying_label":"0"},timeout=False)
	#get validation data
	#pos_cursor_validation = ab.labeled_collection.find({"bullying_label":"1"},timeout=False).skip(400)
	#neg_cursor_validation = ab.labeled_collection.find({"bullying_label":"0"},timeout=False).skip(400)



	for p in pos_cursor_validation:
		pos_validation.append(ab.get_context_vector(p["text"]))
		pos_vlabels.append(1)

	for n in neg_cursor_validation:
		neg_validation.append(ab.get_context_vector(n["text"]))
		neg_vlabels.append(-1)

	for kernel in kernel_list:

		print "Performing SVM for " + kernel + "..."
		degree = 1
		if kernel == "poly":
			degree = 2

		clf = svm.SVC(kernel=kernel, degree = degree, max_iter = 5000000)
		clf.fit(training, tlabels) 

		print "Done Training..."

		print "Validating..."
		
		pos_score = clf.score(pos_validation, pos_vlabels)

		neg_score = clf.score(neg_validation, neg_vlabels)

		total_score = clf.score(pos_validation+neg_validation,pos_vlabels + neg_vlabels)

		scores = {}
		scores["k"] = k
		scores["kernel"] = kernel
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



