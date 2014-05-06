# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import itertools
import string
from scipy import linalg
from sklearn import decomposition

# <codecell>

class CoMatrix:
    # Builds co-occurrence matrix.
    words_to_i = {}
    comat = np.zeros((0,0))   
    u = np.zeros((0,0))
    s = np.zeros((0,0))
    n_components = 0
    
    def reset(self) :
        self.words_to_i = {}
        self.comat = np.zeros((0,0))
    
    def add(self, word_list) :
        """ Given a word_list, which is a list of words, updates the co-occurrence matrix. """
        # First, count the number of new words to re-shape the matrix.
        new_words = [word for word in word_list if word not in self.words_to_i]
        new_words_count = len(new_words)
        
        
        # Re-shape existing co-occurrence matrix to accommodate new words.
        if self.comat.shape[0] is 0 :
            self.comat = np.zeros((new_words_count, new_words_count))
        else:
            cols = np.zeros((self.comat.shape[0], new_words_count))
            rows = np.zeros((new_words_count, self.comat.shape[1] + new_words_count))
            self.comat = np.hstack((self.comat, cols))
            self.comat = np.vstack((self.comat, rows))
        
            
        # Add new words to the map.
        ind = len(self.words_to_i)
        for word in new_words :
            self.words_to_i[word] = ind
            ind += 1
            
        # Update the matrix.
        word_pairs = itertools.product(word_list, word_list)
        for i,j in word_pairs :
            self.comat[self.words_to_i[i], self.words_to_i[j]] += 1
            
        #print self.comat
        
    def do_svd(self, k) :
        """ Does svd and stores the u and s truncated matrices. k is the number of principal dimensions."""
        #self.svd = decomposition.TruncatedSVD(n_components=100, n_iterations=5)
        #self.svd_output = self.svd.fit_transform(self.comat)
        
	self.n_components = k
        self.u,self.s,v = linalg.svd(self.comat)
	#print self.u.shape, self.s.shape
        self.s = np.diag(self.s)
        self.u = self.u[:, 0:k]
        self.s = self.s[0:k, 0:k] 
            
    def projection(self, word) :
        """ For a particular word, simply computes the projection by using the word_th row of u and \
        multiplying with s. """
        if word not in self.words_to_i:
            print np.zeros((0,0))
        else :
            return np.dot(self.u[self.words_to_i[word], :], self.s)
            #return self.svd.transform(self.comat[words_to_i[word]])
            
    def context_vector(self, word_list) :
        """ Given a word_list, computes the corresponding context vector by summing over all the words. """
        c_vector = np.zeros((1,self.n_components))
        for word in word_list :
            pr = self.projection(word)
            if pr.shape[0] == 0 :
                print "Error: word not seen before";
            else :
                c_vector = np.add(c_vector, pr)
        return c_vector

    def test(self):

        """ Testing """
        """ Check simple co-occurrence. """
        word_file = "british-english"
        WORDS = open(word_file).read().splitlines()
        no_words = len(WORDS)

        import random

        m = self
        m.reset()
        for i in range(100) :
            wl1 = [random.choice(WORDS) for i in range(10)]
            wl1.append('cookies')
            wl1.append('biscuits')
            #.append('pastries')
            wl2 = [random.choice(WORDS) for i in range(10)]
            wl2.append('biscuits')
            wl2.append('pastries') 
            m.add(wl1)
            #m.add([random.choice(WORDS) for i in range(10)])
            m.add(wl2)

    def comp_cos(a,b):
        return np.dot(a,b) / ( np.linalg.norm(a) * np.linalg.norm(b))



