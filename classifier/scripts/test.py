import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier
import numpy as np
import pickle

ab = ABClassifier()

#pickle.dump(ab, open('saved_data/ab.p','wb'))

print "Getting data..."
ab.download_cursors(limit_unlabeled = 2500, limit_labeled = 2500)
print "Data received."
print "Performing LSA..."
ab.run_lsa(k=100)
print "LSA Complete."
print "Computing Context Vectors..."
ab.compute_context_vectors()
print "Context Vectors Complete."
print "Saving Context Vectors"

#pickle.dump(ab.pos_labeled_cv_list, open('saved_data/pos_labeled_cv.p','wb'))
#pickle.dump(ab.neg_labeled_cv_list, open('saved_data/neg_labeled_cv.p','wb'))
#pickle.dump(ab.unlabeled_cv_list, open('saved_data/unlabeled_cv.p','wb'))

l = np.array(ab.pos_labeled_cv_list)
m = np.array(ab.neg_labeled_cv_list)
n = np.array(ab.unlabeled_cv_list)
ll = np.asarray(l)
mm = np.asarray(m)
nn = np.asarray(n)

np.savetxt('saved_data/pos_cv_labeled.csv', ll, delimiter=",")
np.savetxt('saved_data/neg_cv_labeled.csv', mm, delimiter=",")
np.savetxt('saved_data/cv_unabeled.csv', nn, delimiter=",")



print "Performing pairwise similarity measures..."

pos_labeled_pws = ab.pairwise_similarity(ab.pos_labeled_cv_list)
neg_labeled_pws = ab.pairwise_similarity(ab.neg_labeled_cv_list)
unlabeled_pws = ab.pairwise_similarity(ab.unlabeled_cv_list)

print "Done."

print "Saving..."

x = np.array(pos_labeled_pws.values())
a = np.asarray(x)
np.savetxt('saved_data/pos_labeled.csv', a, delimiter=",")

y = np.array(neg_labeled_pws.values())
b = np.asarray(y)
np.savetxt('saved_data/neg_labeled.csv', b, delimiter=",")

z = np.array(unlabeled_pws.values())
c = np.asarray(z)
np.savetxt('saved_data/unlabeled.csv', c, delimiter=",")

