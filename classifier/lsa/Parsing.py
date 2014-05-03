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
        word_pairs = itertools.permutations(word_list, 2)
        for i,j in word_pairs :
            CoMatrix.comat[CoMatrix.words_to_i[i], CoMatrix.words_to_i[j]] += 1

        for i in word_list:
            self.comat[self.words_to_i[i], self.words_to_i[i]] += 1


            
        #print CoMatrix.comat

    def add_ones(self):
        # add ones along diag
        CoMatrix.comat = np.add(CoMatrix.comat, np.diag(np.ones((1, CoMatrix.comat.shape[0]))))
        
    def do_svd(self, k) :
        svd = decomposition.TruncatedSVD(n_components=20, n_iterations=10)

        self.svd_output = svd.fit_transform(self.comat)

        """ Does svd and stores the u and s truncated matrices. k is the number of principal dimensions."""
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
word_file = "british-english"
WORDS = open(word_file).read().splitlines()

# <codecell>

no_words = len(WORDS)

# <codecell>

import random

# <codecell>

m = CoMatrix()
m.reset()
for i in range(20) :
    wl1 = [random.choice(WORDS) for i in range(2)]
    wl1.append('cookies')
    wl1.append('biscuits')
    #wl2 = [random.choice(WORDS) for i in range(10)]
    #wl2.append('biscuits')
    #wl2.append('pastries')
    m.add(wl1)
    #m.add(wl2)

#m.add_ones()

# <codecell>

m.comat.shape

# <codecell>

m.do_svd(100)

# <codecell>

vc = m.projection('cookies')

# <codecell>

vb = m.projection('biscuits')
#vp = m.projection('pastries')

# <codecell>

#comp_cos(vc,vp)

# <codecell>

comp_cos(vc,vb)

# <codecell>

uu,ss,vv = linalg.svd(m.comat)

# <codecell>

ssd = np.diag(ss)

# <codecell>

ssd.shape

# <codecell>

ssd

# <codecell>


