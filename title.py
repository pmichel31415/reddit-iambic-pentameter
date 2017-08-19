from __future__ import print_function, division

import sys
import os
from collections import defaultdict
import numpy as np
import numpy.random as npr

import spacy

DETERMINANTS = ['', 'A ', 'The ']
P_DETERMINANTS = [0.4, 0.3, 0.3]


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

    def __init__(self):
        pass

    def initialize(self, nouns_file, adjs_file, determinants=DETERMINANTS, tau=1.0):
        # Load nouns
        self.nouns = load_wordlist(nouns_file)
        # Load adjectives
        self.adjs = load_wordlist(adjs_file)
        # Init spacy
        self.nlp = spacy.load('en')
        # Noun vectors
        self.noun_vectors = np.zeros((len(self.nouns), self.vec_dim))
        for i, noun in enumerate(self.nouns):
            self.noun_vectors[i] = self.nlp(noun).vector
        # Adjectives vectors
        self.adj_vectors = np.zeros((len(self.adjs), self.vec_dim))
        for i, adj in enumerate(self.adjs):
            self.adj_vectors[i] = self.nlp(adj).vector

    def sample_noun(self, vector):
        p = softmax(self.noun_vectors.dot(vector) / self.tau)
        return npr.choice(self.nouns, p=p)

    def sample_adj(self, vector):
        p = softmax(self.adj_vectors.dot(vector) / self.tau)
        return npr.choice(self.adjectives, p=p)

    def sample_det(self, vector):
        return npr.choice(self.nouns, p=P_DETERMINANTS)

    def __call__(self, poem):
        """Generates a title for the input"""
        poem_vector = self.nlp.make_doc(poem).vector
        noun = self.sample_noun(poem_vector)
        adj = self.sample_adjective(poem_vector)
        det = self.sample_det(poem_vector)
        return det + adj + noun

    def save(self, filename):
        np.savez(filename, self.nouns, self.noun_vectors, self.adjs, self.adj_vectors)

    def load(self, filename):
        self.nouns, self.noun_vectors, self.adjs, self.adj_vectors = np.load(filename)


def get_title_generator(options):
    tg = TitleGenerator()
    if options.filename is not None and os.path.isfile(options.filename):
        tg.load(options.filename)
    else:
        tg.initialize(options.nouns_file, options.adjs_file, options.determinants, options.tau)
    return tg
