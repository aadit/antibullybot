"""
   Experiment 2: Compute Pairwise Similarities for 3 Data Sets: 
    -Positive Examples, Negative Examples, Unlabeled
    -Vary the number of input tweets to the Co-Occurrence Matrix
"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


save_location = '../../experiment_data/experiment_2'

k_list = [5, 10, 25, 50, 100, 150, 250, 500]

for k in k_list:
	ab = ABClassifier()
	ab.download_cursors(limit_unlabeled = 1000, limit_labeled = 1000)
	ab.run_lsa(k=k)
	ab.compute_context_vectors(save_location = save_location)

	print "Performing pairwise similarity measures..."

	pos_labeled_pws = cosine_similarity(ab.pos_labeled_cv_list).flatten()
	neg_labeled_pws = cosine_similarity(ab.neg_labeled_cv_list).flatten()
	unlabeled_pws   = cosine_similarity(ab.unlabeled_cv_list).flatten()

	print "Done."

	print "Saving..."

	np.savetxt(save_location + '/pw_pos_' + str(k) + '.csv', pos_labeled_pws, delimiter=",")
	np.savetxt(save_location + '/pw_neg_' + str(k) + '.csv', neg_labeled_pws, delimiter=",")
	np.savetxt(save_location + '/pw_unl_' + str(k) +'.csv', unlabeled_pws, delimiter=",")

	print "Done"

