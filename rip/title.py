# -*- coding: utf-8 -*-
from __future__ import print_function, division

import os
import numpy as np
import numpy.random as npr

import spacy
import util

# Determinants with arbitrary probabilities
DETERMINANTS = ['', 'A ', 'The ']
P_DETERMINANTS = [0.4, 0.3, 0.3]


class TitleGenerator(object):
    """Generates the title of a poem"""

    def __init__(self):
        # Init spacy
        self.nlp = spacy.load('en')

    def initialize(self, nouns_file, adjs_file, determinants=DETERMINANTS, tau=1.0):
        """Initialize the generator"""
        # Save temperature
        self.tau = tau
        # Load nouns
        self.nouns = util.load_wordlist(nouns_file)
        # Load adjectives
        self.adjs = util.load_wordlist(adjs_file)
        # Noun vectors
        self.noun_vectors = np.zeros((len(self.nouns), self.nlp.vocab.vectors_length))
        for i, noun in enumerate(self.nouns):
            self.noun_vectors[i] = self.nlp(noun.decode('utf-8')).vector
        # Adjectives vectors
        self.adj_vectors = np.zeros((len(self.adjs), self.nlp.vocab.vectors_length))
        for i, adj in enumerate(self.adjs):
            self.adj_vectors[i] = self.nlp(adj.decode('utf-8')).vector

    def poem_vector(self, poem):
        """Creates a poem vector"""
        # Feed to spacy (tokenization, POS-tagging)
        doc = self.nlp(poem.decode('utf-8'))
        # Retrieve vectors for nouns
        vectors = [w.vector for w in doc if w.tag_.startswith('NN')]
        # Average noun vectors
        vector = sum(vectors) / len(vectors)
        return vector

    def sample_noun(self, vector):
        """Sample a noun at random.
        The probability of word :math:`w` is
        .. math::
            \log(p(w))\propto w^Tv`

        where :math:`p` is the poem vector and :math:`w` the word vector"""
        p = util.softmax(self.noun_vectors.dot(vector) / self.tau)
        return npr.choice(self.nouns, p=p)

    def sample_adjective(self, vector):
        """Sample an adjective at random (same method as sample_noun)"""
        p = util.softmax(self.adj_vectors.dot(vector) / self.tau)
        return npr.choice(self.adjs, p=p)

    def sample_det(self, adj):
        """Sample a determinant at random"""
        det = npr.choice(DETERMINANTS, p=P_DETERMINANTS)
        # Edge case of a/an (could be better)
        if det == "A " and adj[0] in 'AEIOU':
            det = "An "
        return det

    def __call__(self, poem):
        """Generates a title for the input"""
        poem_vector = self.poem_vector(poem)
        noun = self.sample_noun(poem_vector).capitalize()
        adj = self.sample_adjective(poem_vector).capitalize()
        det = self.sample_det(adj).capitalize()
        return det + adj + " " + noun

    def save(self, filename):
        """Save the noun/adjectives vectors"""
        np.savez(filename,
                 nouns=self.nouns,
                 noun_vectors=self.noun_vectors,
                 adjs=self.adjs,
                 adj_vectors=self.adj_vectors,
                 tau=self.tau)

    def load(self, filename):
        """Load the noun/adjectives vectors"""
        self.__dict__.update(np.load(filename).items())


def get_title_generator(options):
    """Returns a title generator"""
    # Create object
    tg = TitleGenerator()
    if options.filename is not None and os.path.isfile(options.filename):
        # If a saved title generator exists, load from a file
        tg.load(options.filename)
    else:
        # Otherwise initialize from scatch
        tg.initialize(options.nouns_file, options.adjs_file, DETERMINANTS, options.tau)
        tg.save(options.filename if options.filename is not None else 'title_generator')
    return tg
