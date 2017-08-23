# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
from collections import defaultdict
import numpy as np
import numpy.random as npr

import util
import poetry
import curse
import image
import title


class Poet(object):
    """Composes poems (yeah...)"""

    def __init__(self, config_file):
        """Constructor"""
        # Load options
        util.load_config(self, config_file)
        # Set up the collection of verses
        self.verses = load_verses(self.general.output_file)
        self.n_verses = len(self.verses)
        # Store the verses by rhyme
        self.rhymes = defaultdict(lambda: set())
        for i, verse in enumerate(self.verses):
            self.rhymes[poetry.verse_rhyme(verse)].add(i)
        # Total number of rhymes
        self.n_rhymes = len(self.rhymes)
        for k, v in self.rhymes.items():
            self.rhymes[k] = list(v)
        # Probability of picking a rhyme (based on number of such rhymes)
        self.p_rhymes = {r: (len(v) - 1) for r, v in self.rhymes.items()}
        self.names_rhymes, self.p_rhymes = zip(*self.p_rhymes.items())
        self.p_rhymes = np.asarray(self.p_rhymes, dtype=float)
        self.p_rhymes /= self.p_rhymes.sum()
        # Title generator
        self.tg = title.get_title_generator(self.title)

    def add_period(self, line):
        """Adds a period at the end of line"""
        if not line[-1] in '.,!?;':
            line = line + '.'
        elif line[-1] in ',:;':
            line = line[:-1] + '.'
        return line


    def find_rhyming_verse(self, rhyme, verse=None):
        """Finds a random verse that rhymes with the input"""
        # Get all rhyming verses
        rhyming_verses = self.rhymes[rhyme]
        # Until we have a different verse
        # if verse is None this will make sure the rhyming verse is different
        # Sample a rhyming verse
        num_candidates = min(4, len(rhyming_verses))
        candidate_ids = npr.choice(rhyming_verses, size=num_candidates, replace=False)
        candidates = [self.verses[i] for i in candidate_ids]
        if verse is not None:
            for v in candidates:
                if poetry.last_word(verse) != poetry.last_word(v):
                    return v
        return candidates[-1] 

    def sample_rhyming_pair(self, rhyme):
        """Sample a pair of rhyming verses"""
        first_verse = self.find_rhyming_verse(rhyme)
        second_verse = self.find_rhyming_verse(rhyme, verse=first_verse)
        return [first_verse, second_verse]

    def generate_couplet(self):
        """Generates a couplet"""
        # Sample rhymes
        a = npr.choice(self.names_rhymes, p=self.p_rhymes)
        # Get verses
        couplet = self.sample_rhyming_pair(a)
        # Add period at the end
        couplet[-1] = self.add_period(couplet[-1])
        # Package and ship
        return '\n'.join(couplet)

    def generate_quatrain(self):
        """Generate a quatrain"""
        # Sample rhymes
        a, b = npr.choice(self.names_rhymes, size=2, replace=False, p=self.p_rhymes)
        # Get verses
        quatrain = [""] * 4
        quatrain[0], quatrain[2] = self.sample_rhyming_pair(a)
        quatrain[1], quatrain[3] = self.sample_rhyming_pair(b)
        # Add period at the end
        quatrain[-1] = self.add_period(quatrain[-1])
        # Package and ship
        return '\n'.join(quatrain)

    def generate_sonnet(self):
        """Generates a sonnet"""
        # A sonnet is 3 quatrains and one couplet
        sonnet = [""] * 4
        sonnet[0] = self.generate_quatrain()
        sonnet[1] = self.generate_quatrain()
        sonnet[2] = self.generate_quatrain()
        sonnet[3] = self.generate_couplet()
        # Package and ship
        return '\n\n'.join(sonnet)

    def generate_title(self, poem):
        """Generate a title for the poem"""
        return self.tg(poem)

    def add_title(self, poem):
        """Generate a title and prepend it to the string"""
        t = self.generate_title(poem)
        sep = "\n%s\n" % "".join(["-"] * len(t))
        return t + sep + poem


def load_verses(filename):
    """Load verses from dump file created by the bot"""
    verses = []
    with open(filename, 'r') as f:
        for l in f:
            fields = l.strip().split('\t')
            if len(fields) == 6:
                if curse.is_clean(fields[-1]):
                    verses.append(fields[-2].strip())
    return verses


def main():
    config_file = sys.argv[1]
    mode = sys.argv[2]
    poet = Poet(config_file)
    if mode == 'text':
        sonnet = poet.generate_sonnet()
        sonnet = poet.add_title(sonnet)
        print(sonnet)
    elif mode == 'image':
        quatrain = poet.generate_quatrain()
        quatrain = poet.add_title(quatrain)
        image.make_image(quatrain, output_file=sys.argv[3])
    elif mode == 'image_text':
        quatrain = poet.generate_quatrain()
        quatrain = poet.add_title(quatrain)
        image.make_image(quatrain, output_file=sys.argv[3])
        util.savetxt(sys.argv[4], quatrain.split('\n'))
    else:
        print('mode %s not recognized. Here, get a couplet for free:\n' % mode, file=sys.stderr)
        print(poet.generate_couplet(), file=sys.stderr)


if __name__ == '__main__':
    main()
