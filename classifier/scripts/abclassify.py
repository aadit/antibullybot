import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier


ab = ABClassifier()

ab.download_cursors(limit_labeled = 100)
ab.run_lsa(k=100)
ab.compute_context_vectors()

pws = ab.pairwise_similarity(ab.labeled_cv_list)



