import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier


ab = ABClassifier()

ab.download_cursors()
ab.run_lsa(k=100)
ab.compute_context_vectors()



