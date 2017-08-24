# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time
import curse
from subprocess import check_output

import praw

import util
import tweet
import poetry


class RedditIambicPentameterBot(object):
    """A bot capable of identifying iambic pentameters in reddit comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.config_file = config_file
        # Load from yaml config file
        util.load_config(self, config_file)
        # Initialize other relevant variables
        self.n_pentameters = 0
        self.n_length_removed = 0
        self.n_pentameters_epoch = 0
        self.last_tweet = 0
        self.last_quatrain_tweet = 0
        self.start = time.time()
        # Initialize reddit
        self.init_reddit()

    def init_reddit(self):
        """Initialize the reddit instance"""
        # Get reddit instance
        self.r = praw.Reddit(user_agent=self.reddit.user_agent,
                             client_id=self.reddit.client_id,
                             client_secret=self.reddit.secret,
                             username=self.reddit.user_name,
                             password=self.reddit.password)
        # Get r/all/ instance
        self.r_all = self.r.subreddit(self.reddit.subreddit)
        # Get r/R_I_P instance
        self.r_R_I_P = self.r.subreddit('R_I_P')

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
                  '\t%s' % comment.body.strip().replace('\n', '') +  # comment
                  '\t%s' % verse,                                   # clean comment
                  file=f)

    def publish_quatrain(self):
        """Publish a quatrain on social media every given interval"""
        now = time.time()
        if now > self.last_quatrain_tweet + self.twitter.tweet_quatrain_every:
            check_output(["python", "rip/poet.py", self.config_file,
                          "image_text", 'tmp.png', 'tmp.txt'])
            self.tweet_quatrain('tmp.png')
            self.post_quatrain('tmp.txt')
            self.last_quatrain_tweet = time.time()

    def tweet_quatrain(self, img_file):
        """Tweet an image of a quatrain"""
        tweet.tweet_image(img_file, self.twitter)

    def post_quatrain(self, txt_file):
        """Post a quatrain on reddit"""
        # Load the quatrain from a text file
        quatrain = util.loadtxt(txt_file)
        # Get title
        title = quatrain[0]
        # Format as a markdown quote
        text = '\n\n'.join(['> ' + line for line in quatrain[2:]])
        # Post on the r/R_I_P subreddit
        self.r_R_I_P.submit(title, selftext=text)

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
