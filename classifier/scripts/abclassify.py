import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np


ab = ABClassifier()

ab.download_cursors(limit_unlabeled = 1000, limit_labeled = 1000)
ab.run_lsa(k=100)
ab.compute_context_vectors()

labeled_pws = ab.pairwise_similarity(ab.labeled_cv_list)
unlabeled_pws = ab.pairwise_similarity(ab.unlabeled_cv_list)

print "done getting pws"

x = np.array(labeled_pws.values())
a = np.asarray(x)
np.savetxt('x.csv',a,delimiter=",")

y = np.array(unlabeled_pws.values())
b = np.asarray(y)
np.savetxt('y.csv',b,delimiter=",")

