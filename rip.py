from __future__ import print_function, division
import sys
import re

import praw
import time
from collections import defaultdict

import yaml
import string

import poetry

# Filter table to remove all non ascii_lowercase/space characters
filter_table = defaultdict(lambda: None)
for c in string.ascii_lowercase:
    filter_table[c] = unicode(c, 'utf-8')
filter_table[ord(' ')] = u' '


class Attributes(object):
    """A class to access dict fields like object attributes"""

    def __init__(self, dic):
        self.__dict__.update(dic)


class IambicPentameterBot(object):
    """A bot capable of identifying iambic pentameters in reddit comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.load_config(config_file)
        self.n_pentameters = 0
        self.n_length_removed = 0
        self.n_pentameters_epoch = 0

    def load_config(self, config_file):
        """Create fields from yaml file"""
        with open(config_file, 'r') as f:
            data = yaml.load(f)
            for k, v in data.items():
                self.__dict__[k] = Attributes(v)

    def preprocess_comment(self, comment):
        """Preprocess comment to get body without special characters"""
        # lowercase
        candidate = comment.body.strip().lower()
        # Filter punctuation
        return re.sub('[^a-z ]+', '', candidate)

    def is_iambic_pentameter(self, comment):
        """Check if comment is an iambic pentameter"""
        candidate = self.preprocess_comment(comment)
        # Check for length
        if not poetry.length_ok(candidate):
            self.n_length_removed += 1
            return False
        # Check the stress pattern
        pentameter = poetry.detect_iambic_pentameter(candidate, self.poetry.pattern, self.poetry.allow_feminine_rhyme)
        # Save the pentameter
        if pentameter:
            self.save_pentameter(comment, candidate)
            self.n_pentameters += 1
            self.n_pentameters_epoch += 1

    def save_pentameter(self, comment, verse):
        """Saves verse to tsv file with some metadata"""
        with open(self.general.output_file, 'a+') as f:
            print('%d\t/u/%s\t/r/%s\t%s\t%s\t%s' % (time.time(), comment.author, comment.submission.subreddit, comment.submission.over_18, comment.body, verse), file=f)


def main():
    # Instantiate bot
    bot = IambicPentameterBot(sys.argv[1])
    # Get reddit instance
    reddit = praw.Reddit(user_agent=bot.reddit.user_agent,
                         client_id=bot.reddit.client_id,
                         client_secret=bot.reddit.secret,
                         username=bot.reddit.user_name,
                         password=bot.reddit.password)
    # Get subreddit instance
    subreddit = reddit.subreddit(bot.reddit.subreddit)
    # Start looping
    start = time.time()
    i = 0
    for comment in subreddit.stream.comments():
        # Check if comment is and iambic pentameter
        bot.is_iambic_pentameter(comment)
        # Stop if max number of records is reached
        if bot.n_pentameters >= bot.options.max_records:
            break
        # Increment counter
        i += 1
        # Report periodically
        if i >= bot.options.report_every:
            # Print infos
            elapsed = time.time() - start
            percent_length_removed = (bot.n_length_removed) / bot.options.report_every * 100
            print('Analyzed %d comments, %.2f%% too short/long, found %d iambic pentameters (total: %d), %.1f comments/s' %
                  (i, percent_length_removed, bot.n_pentameters_epoch, bot.n_pentameters, i / elapsed))
            sys.stdout.flush()
            # Sleep a bit
            time.sleep(bot.options.sleep_for)
            # Reset periodic counters
            bot.n_length_removed = 0
            bot.n_pentameters_epoch = 0
            i = 0
            start = time.time()


def test():
    bot = IambicPentameterBot(sys.argv[1])
    # Get reddit instance
    reddit = praw.Reddit(user_agent=bot.reddit.user_agent,
                         client_id=bot.reddit.client_id,
                         client_secret=bot.reddit.secret,
                         username=bot.reddit.user_name,
                         password=bot.reddit.password)
    # Get subreddit instance
    test_comment = reddit.comment(id='cqmldc6')
    test_comment.body = 'And cafeteria of other crackers'
    bot.is_iambic_pentameter(test_comment)

if __name__ == '__main__':
    if '--test' in sys.argv:
        test()
    else:
        main()

