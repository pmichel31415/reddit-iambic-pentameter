# Curse words
# (shamelessly taken from github.com/Marjan-GH/Topical_poetry)
curse_words = set()
with open('cursed_words.txt', 'r') as f:
    for l in f:
        curse_words.add(l.strip().lower())


def is_clean(verse):
    """Checks if a verse is clean of curse words (i.e. "twitter safe")"""
    for w in verse.split():
        if w in curse_words:
            return False
    return True
