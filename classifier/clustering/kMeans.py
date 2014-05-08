import sys, random
import math

from time import time

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits


class kMeans:    
    def perform_Kmeans(self, Matrix, k):
        estimator = KMeans(init='k-means++', n_clusters=k, n_init=2)
        estimator.fit(Matrix)
        Result = estimator.predict(Matrix)
        return Result