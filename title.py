from __future__ import print_function, division

import sys
from collections import defaultdict
import numpy as np
import numpy.random as npr

import spacy
from sklearn.neighbors import KNNClassifier

DETERMINANTS= ['', 'A ', 'The ']

def load_wordlist(filename):
    """Load a list of word from a file (one word per line)"""
    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip().lower())
    return words

def softmax(x):
    e = np.exp(x)
    return e / np.sum(e)



class TitleGenerator(object):
    """Generates the title of a poem"""

    def __init__(self, nouns_file, adjs_file, determinants=DETERMINANTS, tau=1.0):
        if os
        
        # Load nouns
        self.nouns = load_wordlist(nouns_file)
        # Load adjectives
        self.adjs = load_wordlist(adjs_file)
        # Init spacy
        self.nlp = spacy.load('en')
        # Noun vectors
        self.noun_vectors = np.zeros((len(self.nouns), self.vec_dim))
        for i, noun in enumerate(nouns):
            self.noun_vectors[i] = self.nlp(noun).vector
        # Adjectives vectors
        self.adj_vectors = np.zeros((len(self.adjs), self.vec_dim))
        for i, adj in enumerate(adjs):
            self.adj_vectors[i] = self.nlp(adj).vector

    def sample_noun(self, vector):
        p = softmax(self.noun_vectors.dot(vector) / self.tau)
        return npr.choice(self.nouns, p=p)

    def sample_adj(self, vector):
        p = softmax(self.adj_vectors.dot(vector) / self.tau)
        return npr.choice(self.adjectives, p=p)

    def sample_det(self, vector):
        
        return npr.choice(self.nouns, p=p)

    def __call__(self, poem):
        """Generates a title for the input"""
        poem_vector = nlp.make_doc(poem).vector
        noun = self.sample_noun(poem_vector)
        adj = self.sample_adjective(poem_vector)
        det = self.sample_det(poem_vector)
