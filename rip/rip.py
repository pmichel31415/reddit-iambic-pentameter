# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time
import curse
from subprocess import check_output

import util
import tweet
import poetry


class RedditIambicPentameterBot(object):
    """A bot capable of identifying iambic pentameters in reddit comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.config_file = config_file
        util.load_config(self, config_file)
        self.n_pentameters = 0
        self.n_length_removed = 0
        self.n_pentameters_epoch = 0
        self.last_tweet = 0
        self.last_quatrain_tweet = 0
        self.start = time.time()

    def tick(self):
        """Get time since last call"""
        elapsed = time.time() - self.start
        self.start = time.time()
        return elapsed

    def preprocess_comment(self, comment):
        """Preprocess comment to get body without special characters"""
        return poetry.preprocess_verse(comment.body)

    def is_iambic_pentameter(self, comment, tweet=True):
        """Check if comment is an iambic pentameter"""
        candidate = self.preprocess_comment(comment)
        # Check for length
        if not poetry.length_ok(candidate):
            self.n_length_removed += 1
            return False
        # Check the stress pattern
        pentameter = poetry.detect_iambic_pentameter(candidate,
                                                     self.poetry.pattern,
                                                     self.poetry.allow_feminine_rhyme)
        # Save the pentameter
        if pentameter:
            self.save_pentameter(comment, candidate)
            if curse.is_clean(candidate) and tweet:
                self.tweet_comment(comment)
            self.n_pentameters += 1
            self.n_pentameters_epoch += 1
            return True
        else:
            return False

    def tweet_comment(self, comment):
        """Tweet the comment (only every self.twitter.tweet_every)"""
        now = time.time()
        if now > self.last_tweet + self.twitter.tweet_every:
            tweet.tweet(tweet.comment_to_tweet(comment), self.twitter)
            self.last_tweet = time.time()

    def save_pentameter(self, comment, verse):
        """Saves verse to tsv file with some metadata"""
        with open(self.general.output_file, 'a+') as f:
            print('%d' % time.time() +                              # timestamp
                  '\t/u/%s' % comment.author +                      # author
                  '\t/r/%s' % comment.submission.subreddit +        # subreddit
                  '\t%s' % comment.submission.over_18 +             # nsfw tag
                  '\t%s' % comment.body.strip().replace('\n', '') + # comment
                  '\t%s' % verse,                                   # clean comment
                  file=f)

    def tweet_quatrain(self):
        """Tweet an image of a quatrain occasionaly"""
        now = time.time()
        if now > self.last_quatrain_tweet + self.twitter.tweet_quatrain_every:
            check_output(["python", "rip/poet.py", self.config_file, "image", 'tmp.png'])
            tweet.tweet_image('tmp.png', self.twitter)
            self.last_quatrain_tweet = time.time()

    def is_done(self):
        """Returns true if the bot has found `max_records` pentameters"""
        return self.n_pentameters >= self.options.max_records

    def process_comment(self, comment):
        """Processes a reddit comment object

        Returns True when no more comment should be processed"""
        # Check for iambic pentameters
        try:
            if self.is_iambic_pentameter(comment):
                # Save comments on reddit just in case
                comment.save()
        except Exception as e:
            print("Failed to process comment: " + str(e), file=sys.stderr)
        # Stop if max number of records is reached
        return self.is_done()
