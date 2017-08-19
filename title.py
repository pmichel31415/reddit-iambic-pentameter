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

vec_dim = 300

class TitleGenerator(object):
    """Generates the title of a poem"""

    def __init__(self):
        pass

    def initialize(self, nouns_file, adjs_file, determinants=DETERMINANTS, tau=1.0):
        # Save temperature
        self.tau = tau
        # Load nouns
        self.nouns = load_wordlist(nouns_file)
        # Load adjectives
        self.adjs = load_wordlist(adjs_file)
        # Init spacy
        self.nlp = spacy.load('en')
        # Noun vectors
        self.noun_vectors = np.zeros((len(self.nouns), vec_dim))
        for i, noun in enumerate(self.nouns):
            self.noun_vectors[i] = self.nlp(noun.decode('utf-8')).vector
        # Adjectives vectors
        self.adj_vectors = np.zeros((len(self.adjs), vec_dim))
        for i, adj in enumerate(self.adjs):
            try:
                self.adj_vectors[i] = self.nlp(adj.decode('utf-8')).vector
            except:
                print(adj)

    def poem_vector(self, poem):
        """Creates a poem vector"""
        doc = self.nlp(poem.decode('utf-8'))
        vectors = [w.vector for w in doc if w.tag_.startswith('NN')]
        vector = sum(vectors) / len(vectors)
        return vector

    def sample_noun(self, vector):
        p = softmax(self.noun_vectors.dot(vector) / self.tau)
        return npr.choice(self.nouns, p=p)

    def sample_adjective(self, vector):
        p = softmax(self.adj_vectors.dot(vector) / self.tau)
        return npr.choice(self.adjs, p=p)

    def sample_det(self, vector):
        return npr.choice(DETERMINANTS, p=P_DETERMINANTS)

    def __call__(self, poem):
        """Generates a title for the input"""
        poem_vector = self.poem_vector(poem)
        noun = self.sample_noun(poem_vector).capitalize()
        adj = self.sample_adjective(poem_vector).capitalize()
        det = self.sample_det(poem_vector).capitalize()
        return det + adj + " " + noun

    def save(self, filename):
        np.savez(filename, self.nouns, self.noun_vectors, self.adjs, self.adj_vectors)

    def load(self, filename):
        self.nouns, self.noun_vectors, self.adjs, self.adj_vectors = np.load(filename)


def get_title_generator(options):
    tg = TitleGenerator()
    if options.filename is not None and os.path.isfile(options.filename):
        tg.load(options.filename)
    else:
        tg.initialize(options.nouns_file, options.adjs_file, DETERMINANTS, options.tau)
    return tg
