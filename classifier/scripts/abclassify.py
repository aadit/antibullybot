import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np


ab = ABClassifier()

ab.download_cursors(limit_unlabeled = 1000, limit_labeled = 1000)
ab.run_lsa(k=100)
ab.compute_context_vectors()

pws = ab.pairwise_similarity(ab.labeled_cv_list)


print "done getting pws"

x = np.array(pws.values())
a = np.asarray(x)
np.savetxt('x.csv',a,delimiter=",")



