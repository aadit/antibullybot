"""
   Experiment 10: Threshold Classification:
   -Compute SVDs
   -Compute average pos/neg 
   -Compute pairwise similarity pw(tweet, pos) pw(tweet, neg)
   -Classify Tweet on higher similarity measure (or threshold?)
   -Uses ONLY twitter data for testing/validation
"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import sklearn as sk
import random
from sklearn.metrics.pairwise import cosine_similarity
import os



save_location = '../../experiment_data/experiment_10'
limit_1 = 400 #validation set
limit_2 = 400 #training set

k = 150

thresholds = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85]
results = {}
for t in thresholds:
	results_obj = {}
	results_obj['t'] = t
	results_obj['pos_list_size'] = 0
	results_obj['neg_list_size'] = 0
	results_obj['true_pos'] = 0
	results_obj['true_neg'] = 0
	results_obj['true_pos_rate'] = 0
	results_obj['true_neg_rate'] = 0
	results_obj['accuracy'] = 0
	results_obj['num_iterations'] = 0
	results[int(t*100)] = results_obj

ab = ABClassifier()
ab.download_tweet_cursors(limit_unlabeled = 2500, limit_labeled = 2500)
ab.run_lsa(k=k)


for i in xrange(0,1):
	for t in thresholds:

		print "Running experiment for t = " + str(t)
		print "Starting classification..."

		unlabeled_cursor   = ab.db.tweets.find({"bullying_label" : {'$exists' :True}}, timeout = False).limit(limit_1)
		pos_cursor = ab.labeled_collection.find({"bullying_label":"1"},timeout=False).skip(limit_1).limit(limit_2)
		neg_cursor = ab.labeled_collection.find({"bullying_label":"0"},timeout=False).skip(limit_1).limit(limit_2)


		p_avg = np.zeros(k)
		n_avg = np.zeros(k)
		for p,n in zip(pos_cursor, neg_cursor):

			p_avg = p_avg + ab.get_context_vector(p["text"])

			n_avg = n_avg + ab.get_context_vector(n["text"])

		p_avg = p_avg/limit_1
		n_avg = n_avg/limit_1


		positive_set = []
		negative_set = []

		for u in unlabeled_cursor:

			u_obj = {}
			u_obj["text"] = u["text"]
			u_obj["cv"]   = ab.get_context_vector(u_obj["text"])
			u_obj["bullying_label"] = u["bullying_label"]

			pos_similarity = cosine_similarity(p_avg, u_obj["cv"])[0][0]
			neg_similarity = cosine_similarity(n_avg, u_obj["cv"])[0][0]

			#if pos_similarity > neg_similarity:
				#positive_set.append(u_obj)

			if pos_similarity >= t:
				positive_set.append(u_obj)

			else:
				negative_set.append(u_obj)

		positive_file = open(save_location + "/positive_set_" + str(t) + ".txt", 'wb')
		negative_file = open(save_location + "/negative_set_" + str(t) + ".txt", 'wb')
		false_positive_file = open(save_location + "/false_positive_set_"+ str(t) + ".txt", "wb")
		false_negative_file = open(save_location + "/false_negative_set_"+ str(t) + ".txt", "wb")


		true_pos = 0
		true_neg = 0

		for p in positive_set:
			print >> positive_file, p["text"].encode('utf-8')
			if p["bullying_label"] == "1":
				true_pos = true_pos + 1
			else:
				print >> false_positive_file, p["text"].encode('utf-8')


		for n in negative_set:
			print >> negative_file, n["text"].encode('utf-8')
			if n["bullying_label"] == "0":
				true_neg = true_neg + 1
			else:
				print >> false_negative_file, n["text"].encode('utf-8')


		positive_file.close()
		negative_file.close()
		false_positive_file.close()
		false_negative_file.close()
		#compute results
		t = int(100*t)
		results_obj = results[t]
		i = results[t]['num_iterations']
		results_obj['pos_list_size'] = float(len(positive_set) + results[t]['pos_list_size'] * i)/(i+1)
		results_obj['neg_list_size'] = float(len(negative_set) + results[t]['neg_list_size'] * i)/(i+1)
		results_obj['true_pos'] = float(true_pos + results[t]['true_pos'] * i)/(i+1)
		results_obj['true_neg'] = float(true_neg + results[t]['true_neg'] * i)/(i+1)
		results_obj['true_pos_rate'] = float(results_obj['true_pos'])/results_obj['pos_list_size']
		results_obj['true_neg_rate'] = float(results_obj['true_neg'])/results_obj['neg_list_size']
		results_obj['accuracy'] = float(results_obj['true_pos'] + results_obj['true_neg'])/(results_obj['pos_list_size'] + results_obj['neg_list_size'])
		results_obj['num_iterations'] = i + 1
		results[t] = results_obj

		"Done. Files saved at " + save_location


for t in thresholds:
	r = results[int(t*100)]
	print " " 
	print "t: %f" % (r["t"])
	print "num positive: %i " % (r["pos_list_size"])
	print "num negative: %i" % (r["neg_list_size"])
	print "true pos rate: %f" % (r['true_pos_rate'])
	print "true neg rate: %f" % (r['true_neg_rate'])
	print "accuracy: %f" % (r["accuracy"])


os.system('say "Done with your script!"')







