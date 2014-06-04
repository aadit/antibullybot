"""
   Experiment 9: Compute Pairwise Similarities for 3 Data Sets: 
    -Positive Examples, Negative Examples, Unlabeled
    -Vary the number of input tweets to the Co-Occurrence Matrix
    -Uses ONLY twitter data for training/validation

"""


import sys
sys.path.append('../..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import os

save_location = '../../experiment_data/experiment_9'

ab = ABClassifier()
ab.download_tweet_cursors(limit_unlabeled = 2500, limit_labeled = 2500)
ab.run_lsa(k=150)
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

os.system('say "Done with your script!"')
