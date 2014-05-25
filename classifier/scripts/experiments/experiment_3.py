"""
   Experiment 3: Simple Classification:
   -Draw random unlabeled tweet, pos, and neg examples
   -Compute Context Vectors for all 3
   -Compute pairwise similarity pw(tweet, pos) pw(tweet, neg)
   -Classify Tweet on higher similarity measure (or threshold?)
"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import sklearn as sk
import random
from sklearn.metrics.pairwise import cosine_similarity



save_location = '../../experiment_data/experiment_3'
limit_1 = 2500
limit_2 = 250

k_list = [5, 10, 25, 50, 100, 150, 200]

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

	positive_set = []
	negative_set = []

	for u in unl:

		p = random.choice(pos)
		n = random.choice(neg)

		pos_similarity = cosine_similarity(p["cv"], u["cv"])[0][0]
		neg_similarity = cosine_similarity(n["cv"], u["cv"])[0][0]

		if pos_similarity > neg_similarity:
			positive_set.append(u["text"])

		else:
			negative_set.append(u["text"])

	positive_file = open(save_location + "/positive_set_" + str(k) + ".txt", 'wb')
	negative_file = open(save_location + "/negative_set_" + str(k) + ".txt", 'wb')


	for p in positive_set:
		print >> positive_file, p.encode('utf-8')

	for n in negative_set:
		print >> negative_file, n.encode('utf-8')

	positive_file.close()
	negative_file.close()

	"Done. Files saved at " + save_location









