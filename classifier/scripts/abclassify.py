import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np


ab = ABClassifier()

ab.download_cursors(limit_unlabeled = 1000, limit_labeled = 1000)
ab.run_lsa(k=100)
ab.compute_context_vectors()

pos_labeled_pws = ab.pairwise_similarity(ab.pos_labeled_cv_list)
neg_labeled_pws = ab.pairwise_similarity(ab.neg_labeled_cv_list)
unlabeled_pws = ab.pairwise_similarity(ab.unlabeled_cv_list)

print "done getting pws"

x = np.array(pos_labeled_pws.values())
a = np.asarray(x)
np.savetxt('pos_labeled.csv', a, delimiter=",")

y = np.array(neg_labeled_pws.values())
b = np.asarray(y)
np.savetxt('neg_labeled.csv', b, delimiter=",")

z = np.array(unlabeled_pws.values())
c = np.asarray(z)
np.savetxt('unlabeled.csv', c, delimiter=",")

