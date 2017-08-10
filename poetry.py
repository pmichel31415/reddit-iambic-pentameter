from __future__ import division
import re

import pronouncing as pr

# An iambic pentameter has 10-11 syllables, syllables rarely have
# less than 2 characters and more than 3
MIN_CHARS = 15
MAX_CHARS = 40

# Dictionnary matching 2 to 1 in stress patterns
two_to_one_stress = {ord('2'): u'1'}


def length_ok(candidate):
    """Returns whether the candidate has a length compatible with the iambic pentameter"""
    # Count number of characters (without spaces)
    length = sum(map(len, candidate.split()))
    # Check whether the count is in [MIN_CHARS, MAX_CHARS]
    return length >= MIN_CHARS and length <= MAX_CHARS


def preprocess_verse(verse):
    """Lowercase and filter all punctuation"""
    # lowercase
    verse_lower = verse.strip().lower()
    # Filter punctuation
    return re.sub('[^a-z ]+', '', verse_lower)


def detect_iambic_pentameter(candidate, pattern='01010101010', allow_feminine_rhyme=True):
    """Detects whether the candidate sentence matches the iambic pentameter stress pattern"""
    # Iterate over words
    for w in candidate.split():
        # Remaining syllables
        L = len(pattern)
        # Start looping over possible stress patterns of current word
        found_pattern = False
        for s in pr.stresses_for_word(w):
            # Identify type 2 stresses with type 1
            s = s.translate(two_to_one_stress)
            # Number of syllables of the word
            l_s = len(s)
            # Trick from (Ghazvininejad et al., 2016)
            if l_s > 2 and s[-3:] == '100':
                s = '%s%s' % (s[:-1], '1')
            # check whether the stress patterns match
            if l_s <= L and pattern.find(s, 0, l_s) == 0:
                # if yes, reduce the target pattern and get to next word
                pattern = pattern[l_s:]
                found_pattern = True
                break
        # If no matching stress pattern was found for this word, return false
        if not found_pattern:
            return False
    # If there are more syllables remaining (not counting the feminine rhyme)
    if len(pattern) > 1 or (not allow_feminine_rhyme and len(pattern) == 1):
        return False
    # Return the iambic pentameter
    return candidate


def verse_rhyme(verse):
    """Gets the rhyme of a verse"""
    # Get last word
    last_word = preprocess_verse(verse).split()[-1]
    # Get last two phones
    phones = pr.phones_for_word(last_word)[0].split()
    rhyme = phones[-1] if len(phones) == 1 else ''.join(phones[-2:])
    return rhyme
