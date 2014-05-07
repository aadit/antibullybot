import sys, random
import math

from time import time

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits

class Point:
    def __init__(self, coords, reference=None):
        self.coords = coords
        self.n = len(coords)
        self.current = 0
        self.reference = reference
    def __repr__(self):
        return str(self.coords)
	def __iter__(self):
		return self
	def __next__(self):
		if self.current >= self.n:
			self.current = 0
			raise StopIteration
		else:
			self.current += 1
			return self.current - 1

def makeRandomPoint(n, lower, upper):
    l = [random.uniform(lower, upper) for i in range(n)]
    return Point(l)

num_points, dim, k, cutoff, lower, upper = 5, 2, 2, 30, 0, 200
points = map( lambda i: makeRandomPoint(dim, lower, upper), range(num_points) )

Matrix = [[0 for x in xrange(dim)] for x in xrange(num_points)] 

for i in range(num_points):
    j = 0
    for j in range(dim):
        Matrix[i][j]=points[i].coords[j]
        print Matrix[i][j]

estimator = KMeans(init='k-means++', n_clusters=k, n_init=2)
estimator.fit(Matrix)

Result = estimator.predict(Matrix)

for l in range(num_points):
    print Result[l]

print "worked"