import sys
sys.path.append('..')
from ABClassifier.ABClassifier import ABClassifier
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np


ab = ABClassifier()

ab.download_cursors(limit_unlabeled = 1000, limit_labeled = 1000)
ab.run_lsa(k=100)
ab.compute_context_vectors()

pws = ab.pairwise_similarity(ab.labeled_cv_list)

x = np.array(pws.values())

num_bins = 100

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Cosine Similarity')
ax1.set_ylabel('Relative Frequency')
ax1.set_title('Cosine Similarity in Bully Data')
ax1.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
plt.show()
