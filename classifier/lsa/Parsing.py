import numpy as np
import itertools
import string
from scipy import linalg
from scipy import sparse
from sklearn import decomposition


class CoMatrix:
    # Builds co-occurrence matrix.
    freq_dict = {}
    words_to_i = {}
    comat = np.zeros((0,0))   
    u = np.zeros((0,0))
    s = np.zeros((0,0))
    n_components = 0
    
    def reset(self) :
        self.words_to_i = {}
        self.comat = np.zeros((0,0))
        self.freq_dict = {}
    
    def add(self, word_list) :
        word_pairs = itertools.product(set(word_list), set(word_list))
        ind = len(self.words_to_i)
        for w in word_list :
            if w not in self.words_to_i :
                self.words_to_i[w] = ind
                ind += 1
        for pair in word_pairs :
            if pair in self.freq_dict :
                self.freq_dict[pair] += 1
            else :
                self.freq_dict[pair] = 1 

    def sparsify(self) :
        # Construct `dense' matrix
        self.comat = np.zeros((len(self.words_to_i), len(self.words_to_i)))
        for x,y in self.freq_dict :
            self.comat[self.words_to_i[x],self.words_to_i[y]] = self.freq_dict[x,y]
        # Sparsify 
        self.comat = sparse.coo_matrix(self.comat)

    def do_svd(self, k) :
        """ Does svd and stores the u and s truncated matrices. k is the number of principal dimensions."""
        #self.svd = decomposition.TruncatedSVD(n_components=100, n_iterations=5)
        #self.svd_output = self.svd.fit_transform(self.comat)

        # check for sparseness
        self.sparsify()
        self.n_components = k
        self.u,self.s,v = sparse.linalg.svds(self.comat, k=self.n_components)

        #print self.u.shape, self.s.shape
        self.singular_values = self.s
        self.s_untruncated = np.diag(self.s)
        self.s = np.diag(self.s)
        '''self.s_untruncated = np.diag(self.s)
        self.u = self.u[:, 0:k]
        self.s = self.s_untruncated[0:k, 0:k]  '''

            
    def get_projection(self, word) :
        """ For a particular word, simply computes the projection by using the word_th row of u and \
        multiplying with s. """
        if word not in self.words_to_i:
            return np.zeros((0,0))
        else :
            return np.dot(self.u[self.words_to_i[word], :], self.s)
            #return self.svd.transform(self.comat[words_to_i[word]])
            
    def get_context_vector(self, word_list) :
        """ Given a word_list, computes the corresponding context vector by summing over all the words. """
        c_vector = np.zeros(self.n_components)
        for word in word_list :
            pr = self.get_projection(word)
            if pr.shape[0] == 0 :
                #print "Error: word not seen before"
                pass
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



