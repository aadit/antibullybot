# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import itertools
import string

# <codecell>

class CoMatrix:
    ' Builds co-occurrence matrix.'
    words_to_i = {}
    comat = np.zeros((0,0))   
    
    def reset(self) :
        CoMatrix.words_to_i = {}
        CoMatrix.comat = np.zeros((0,0))
    
    def add(self, word_list) :
        ' First, count the number of new words to re-shape the matrix.'
        new_words = [word for word in word_list if word not in CoMatrix.words_to_i]
        new_words_count = len(new_words)
        
        
        ' Re-shape existing co-occurrence matrix to accommodate new words.'
        if CoMatrix.comat.shape[0] is 0 :
            CoMatrix.comat = np.zeros((new_words_count, new_words_count))
        else:
            cols = np.zeros((CoMatrix.comat.shape[0], new_words_count))
            rows = np.zeros((new_words_count, CoMatrix.comat.shape[1] + new_words_count))
            CoMatrix.comat = np.hstack((CoMatrix.comat, cols))
            CoMatrix.comat = np.vstack((CoMatrix.comat, rows))
        
            
        ' Add new words to the map.'
        ind = len(CoMatrix.words_to_i)
        for word in new_words :
            CoMatrix.words_to_i[word] = ind
            ind += 1
            
        ' Update the matrix.'
        word_pairs = itertools.permutations(word_list, 2)
        for i,j in word_pairs :
            CoMatrix.comat[CoMatrix.words_to_i[i], CoMatrix.words_to_i[j]] += 1
            
        'print CoMatrix.comat'
        
        

# <codecell>

' Debugging cell.'

text = "Thousands of good, calm, bourgeois faces thronged the windows, the doors, the dormer windows, the roofs, \
gazing at the palace, gazing at the populace, and asking nothing more; for many Parisians content themselves with the \
spectacle of the spectators, and a wall behind which something is going on becomes at once, for us, a very curious \
thing indeed"
text = "apple banana mango grape"
text2 = ['apple', 'banana', 'melon']
exclude = set(string.punctuation)
p_text = ''.join(ch for ch in text if ch not in exclude).split()
m = CoMatrix()
m.reset()
m.add(p_text)
m.add(text2)

# <codecell>

' Do SVD.'
u,s,v = np.linalg.svd(m.comat)

# <codecell>

def project(word_vector, u,s,v,k) :
    ' Figure out how this works.'

def context_vector(mat, word_to_i, tweet, u, s,v, k) :
    ' Computes the context_vector of a tweet. *mat* is the co-occurrence matrix\
    *word_to_i* is the word-to-index hash map, *tweet* is the list of words in the \
    current tweet, *u,s,v* is the SVD of *mat.comat* and, *k* is the number of \
    principal singular vectors.'
    
    'check dimensions'
    c_vector = np.zeros((1,k))     
    for word in tweet :
        c_vector = np.add(c_vector, project(mat[word_to_i[word], :], u,s,v,k))     
        
    return c_vector

