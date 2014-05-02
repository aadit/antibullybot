import sys, random
import math
from itertools import izip

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

class Cluster:
    def __init__(self, points):
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        self.points = points
        self.n = points[0].n
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")
        self.centroid = self.calculateCentroid()
    def __repr__(self):
        return str(self.points)
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        return getDistance(old_centroid, self.centroid)
    def calculateCentroid(self):
        reduce_coord = lambda i:reduce(lambda x,p : x + p.coords[i],self.points,0.0)    
        centroid_coords = [reduce_coord(i)/len(self.points) for i in range(self.n)] 
        return Point(centroid_coords)

def kmeans(points, k, cutoff):
    initial = random.sample(points, k)
 #   print initial
    clusters = [Cluster([p]) for p in initial]
    iterate = 0
    while iterate < 100:
 #       print "Iteration Number ", iterate
        lists = [ [] for c in clusters]
        for p in points:
            largest_cosine = cosine_measure(p,clusters[0].centroid)
            index = 0
            for i in range(len(clusters[1:])):
                distance = cosine_measure(p, clusters[i+1].centroid)
                if distance > largest_cosine:
                    largest_cosine = distance
                    index = i+1
            lists[index].append(p)
        biggest_shift = 0.0
        for i in range(len(clusters)):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        iterate = iterate + 1
 #       print "Iteration ", biggest_shift
 #       if biggest_shift < cutoff: 
 #           break
    return clusters

def getDistance(a, b):
    if a.n != b.n: raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)
	
def cosine_measure(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
 #   print v1.coords[0], " ", v2.coords[0], " " , prod / (len1 * len2)
    return prod / (len1 * len2)

def dot_product(v1, v2):
    sum = 0
    for i in range(v1.n):
        sum = sum + v1.coords[i]*v2.coords[i]
#    return sum(map(lambda x: x[0] * x[1], izip(v1, v2)))
    return sum
	
def makeRandomPoint(n, lower, upper):
    l = [random.uniform(lower, upper) for i in range(n)]
    return Point(l)

def main():
    num_points, dim, k, cutoff, lower, upper = 100, 100, 2, 30, 0, 200
    points = map( lambda i: makeRandomPoint(dim, lower, upper), range(num_points) )
    
 
    
    reverseList = []
    NumberPoints = len(points)
    for j in range(NumberPoints):
        for l in range(len(points[j].coords)):
            reverseList.append(points[j].coords[l]*-1)
        p1 = Point (reverseList)
        points.append(p1)
        reverseList = []


 #   print len(points)
    clusters = kmeans(points, k, cutoff)

    for i,c in enumerate(clusters): 
        for p in c.points:
            print " Cluster: ",i ,"\t Point :", p.coords[0] 

if __name__ == "__main__": 
    main()