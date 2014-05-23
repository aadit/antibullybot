"""
   Experiment 1: Compute Pairwise Similarities for 3 Data Sets: 
   Posiitive Examples, Negative Examples, Unlabeled
"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import pickle

save_location = '../../experiment_data/experiment_1'

ab = ABClassifier()
ab.download_cursors(limit_unlabeled = 250, limit_labeled = 250)
ab.run_lsa(k=100)
ab.compute_context_vectors(save_location = save_location)

print "Performing pairwise similarity measures..."

pos_labeled_pws = ab.pairwise_similarity(ab.pos_labeled_cv_list)
neg_labeled_pws = ab.pairwise_similarity(ab.neg_labeled_cv_list)
unlabeled_pws   = ab.pairwise_similarity(ab.unlabeled_cv_list)

print "Done."


print "Saving..."

x = np.array(pos_labeled_pws.values())
a = np.asarray(x)
np.savetxt(save_location + '/pw_pos.csv', a, delimiter=",")

y = np.array(neg_labeled_pws.values())
b = np.asarray(y)
np.savetxt(save_location + '/pw_neg.csv', b, delimiter=",")

z = np.array(unlabeled_pws.values())
c = np.asarray(z)
np.savetxt(save_location + '/pw_unl.csv', c, delimiter=",")

print "Done"

