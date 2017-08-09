import pronouncing as pr

# An iambic pentameter has 10-11 syllables, syllables rarely have less than 2 characters and more than 3
MIN_CHARS = 15
MAX_CHARS = 40

# Dictionnary matching 2 to 1 in stress patterns
two_to_one_stress = {ord('2'): '1'}


def length_ok(candidate):
    """Returns whether the candidate has a length compatible with the iambic pentameter"""
    # Count number of characters (without spaces)
    length = sum(map(len, candidate.split()))
    # Check whether the count is in [MIN_CHARS, MAX_CHARS]
    return length >= MIN_CHARS and length <= MAX_CHARS


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
            l = len(s)
            # check whether the stress patterns match
            if l <= L and pattern.find(s, 0, l) == 0:
                # if yes, reduce the target pattern and get to next word
                pattern = pattern[l:]
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
