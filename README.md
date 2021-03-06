<div align="center">
  <a href="https://pmichel31415.github.io/reddit-iambic-pentameter/">
    <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/images/logo.gif" width="100px">
  </a>
</div>

#  [RIP: Reddit Iambic Pentameters](https://pmichel31415.github.io/reddit-iambic-pentameter/)

RIP is a bot that scans new comment on the popular message board [reddit](https://www.reddit.com/r/all/) to detect iambic pentameter, one of the most famous types of verses in english poetry.

Here are some funny quartains it composed:

<div align="center">
  <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/images/the_conventional_beyond.png" width="300px">
</div>
<div align="center">
  <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/images/the_christian_zoo.png" width="300px">
</div>

RIP tweets an Iambic pentameter found on twitter every 2 hours, [follow him!](https://twitter.com/R_I_P_bot)

Every 3 hours it composes a quatrain (4 verses with alternating rhymes) and publishes it on [twitter](https://twitter.com/R_I_P_bot) and its own subreddit, [/r/R_I_P](https://www.reddit.com/r/R_I_P/)

## Iambic pentameters?

From wikipedia:

> An iambic foot is an unstressed syllable followed by a stressed syllable. [...] A standard line of iambic pentameter is five iambic feet in a row

Here's an example of a iambic pentameter that you would typically encounter on reddit:

> That second post was hard to understand 

This line follows the ``0101010101`` stress pattern, here's a breakdown

    That | se | cond | post | was | hard | to | un | der | stand
      0    1     0      1      0     1     0    1     0      1  

In practice some words (especially stop words like "the" or "a") might have different stresses depending on the context. For now RIP accepts as iambic pentameter any comment where at least one sequence of stresses matches the iambic pentameter template. This means some verses might sound a bit "off", but we'll assume this is poetic licence :).

## Poem generation

RIP uses the pentameters retrieved on reddit to compose fun (and often nonsensical) poems. The code for poem generation is in the [poet.py](rip/poet.py) file.

### Generating rhymes

A rhyme is assigned to each comment stored by RIP. For the purpose of this bot, a rhyme is defined to be the last phonemes in the sentence, starting from the last vowel.

Example:

    doubt -> D AW1 T -> "AW1T"
    proletariat -> P R OW2 L AH0 T EH1 R IY0 AH0 T -> "AH0T"

Given one verse, RIP just samples a second verse amongst all the rhyming verses. Some techniques are implemented to prevent the rhyming verses from being too similar (like having the same last word), the details of which you can find in [poet.py](rip/poet.py).

### Generating poems

Poems based on iambic pentameters can then be generated by sampling pairs of rhyming verses and arranging them accordingly. Three types of poems are implemented as of now:

- Couplet: just a pair of rhyming verses
- Quatrain: four verses with alternating rhymes
- Sonnet: three quatrains and one couplet

### Adding a title

RIP also generates titles for its poems. Instead of just using purely random words, RIP uses word vectors called [GloVe](https://nlp.stanford.edu/projects/glove/).

Without going into too much details, word vectors associate each word with a 300 dimensional vector. These vectors have the nice property that their dot product somewhat correlates with the semantic similarity between words, ie

<div align="center">
  <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/images/glove_dot.png" height="50px">
</div>

We construct a vector representation for the poem by averaging the word vectors for all the nouns in the poem (kind of getting the "average topic" of the poem). We then sample a noun and an adjective from a predefined list to form a title.

We choose the noun and adjective to be close to the topic of the poem. This means that we want the (logarithmic) probability of sampling e.g. noun "Zoo" to be proportional to the dot produt between the poem vector and the word vector for "Zoo".

For math savvy readers this can be written as:

<div align="center">
  <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/images/noun_log_prob.png" height="50px">
</div>

In practice this gives relatively good results.

## Requirements

RIP requires a bunch of packages to run:

    numpy>=1.11.0       # For all the math and random number generation
    Pillow>=4.2.1       # To convert text to images
    spacy>=1.8.2        # For the title generation (POS tagging, word vectors)
    tweepy>=3.5.0       # Interface to the twitter API
    PyYAML>=3.12        # For the yaml config files
    praw>=5.0.1         # Interface to the reddit API
    pronouncing>=0.1.5  # To get rhyme/stress patterns in words

## Usage

Modify the config file to set your bot's details. Then just run

```bash
python run.py config.yaml
```
