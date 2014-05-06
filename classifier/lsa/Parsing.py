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
    
    def reset(self) :
        CoMatrix.words_to_i = {}
        CoMatrix.comat = np.zeros((0,0))
    
    def add(self, word_list) :
        """ Given a word_list, which is a list of words, updates the co-occurrence matrix. """
        # First, count the number of new words to re-shape the matrix.
        new_words = [word for word in word_list if word not in CoMatrix.words_to_i]
        new_words_count = len(new_words)
        
        
        # Re-shape existing co-occurrence matrix to accommodate new words.
        if CoMatrix.comat.shape[0] is 0 :
            CoMatrix.comat = np.zeros((new_words_count, new_words_count))
        else:
            cols = np.zeros((CoMatrix.comat.shape[0], new_words_count))
            rows = np.zeros((new_words_count, CoMatrix.comat.shape[1] + new_words_count))
            CoMatrix.comat = np.hstack((CoMatrix.comat, cols))
            CoMatrix.comat = np.vstack((CoMatrix.comat, rows))
        
            
        # Add new words to the map.
        ind = len(CoMatrix.words_to_i)
        for word in new_words :
            CoMatrix.words_to_i[word] = ind
            ind += 1
            
        # Update the matrix.
        word_pairs = itertools.product(word_list, word_list)
        for i,j in word_pairs :
            CoMatrix.comat[CoMatrix.words_to_i[i], CoMatrix.words_to_i[j]] += 1
            
            
        #print CoMatrix.comat
        
    def do_svd(self, k) :
        """ Does svd and stores the u and s truncated matrices. k is the number of principal dimensions."""
        #CoMatrix.svd = decomposition.TruncatedSVD(n_components=100, n_iterations=5)
        #CoMatrix.svd_output = CoMatrix.svd.fit_transform(CoMatrix.comat)
        
        CoMatrix.u,CoMatrix.s,v = linalg.svd(CoMatrix.comat)
        CoMatrix.s = np.diag(CoMatrix.s)
        CoMatrix.u = CoMatrix.u[:, 0:k]
        CoMatrix.s = CoMatrix.s[0:k, 0:k] 
            
    def projection(self, word) :
        """ For a particular word, simply computes the projection by using the word_th row of u and \
        multiplying with s. """
        if word not in CoMatrix.words_to_i:
            print np.zeros((0,0))
        else :
            return np.dot(CoMatrix.u[CoMatrix.words_to_i[word], :], CoMatrix.s)
            #return CoMatrix.svd.transform(CoMatrix.comat[words_to_i[word]])
            
    def context_vector(self, word_list) :
        """ Given a word_list, computes the corresponding context vector by summing over all the words. """
        c_vector = np.zeros((1,k))
        for word in word_list :
            pr = projection(word)
            if pr.shape[0] == 0 :
                print "Error: word not seen before";
            else :
                c_vector = np.add(c_vector, pr)
        return c_vector
        
    

# <codecell>

def comp_cos(a,b) :
    return np.dot(a,b) / ( np.linalg.norm(a) * np.linalg.norm(b))

# <codecell>

""" Testing """
""" Check simpel co-occurrence. """
word_file = "/usr/share/dict/british-english"
WORDS = open(word_file).read().splitlines()

# <codecell>

no_words = len(WORDS)

# <codecell>

import random

# <codecell>

m = CoMatrix()
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

# <codecell>


