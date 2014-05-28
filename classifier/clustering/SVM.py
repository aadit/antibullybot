import sys, random
import math

from time import time
from sklearn import svm
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.datasets import load_digits


class SVM:
    def __init__(self):
        self.clf = svm.SVC()
        
    def generate_model(self,testingData, classes):
        self.clf = self.clf.fit(testingData, classes)
        SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
        gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
        shrinking=True, tol=0.001, verbose=False)

    def predict(self,datapoints):
        return (self.clf.predict(datapoints))