from __future__ import print_function, division

import sys
import time
import curse
from subprocess import check_output

import praw
import yaml

import tweet
import poetry


class Attributes(object):
    """A class to access dict fields like object attributes"""

    def __init__(self, dic):
        self.__dict__.update(dic)


class RedditIambicPentameterBot(object):
    """A bot capable of identifying iambic pentameters in reddit comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.load_config(config_file)
        self.n_pentameters = 0
        self.n_length_removed = 0
        self.n_pentameters_epoch = 0
        self.last_tweet = 0
        self.last_quatrain_tweet = 0

    def load_config(self, config_file):
        """Create fields from yaml file"""
        with open(config_file, 'r') as f:
            data = yaml.load(f)
            for k, v in data.items():
                self.__dict__[k] = Attributes(v)

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
            print('%d' % time.time() +                          # timestamp
                  '\t/u/%s' % comment.author +                  # author
                  '\t/r/%s' % comment.submission.subreddit +    # subreddit
                  '\t%s' % comment.submission.over_18 +         # nsfw tag
                  '\t%s' % comment.body.strip() +               # comment
                  '\t%s' % verse,                               # clean comment
                  file=f)

    def tweet_quatrain(self):
        """Tweet an image of a quatrain occasionaly"""
        now = time.time()
        if now > self.last_quatrain_tweet + self.twitter.tweet_quatrain_every:
            check_output(["python", "poet.py", self.general.output_file, "image", 'tmp.png'])
            tweet.tweet_image('tmp.png', self.twitter)
            self.last_quatrain_tweet = time.time()


def main():
    # Instantiate bot
    bot = RedditIambicPentameterBot(sys.argv[1])
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
        try:
            if bot.is_iambic_pentameter(comment):
                # Save comments on reddit just in case
                comment.save()
        except Exception, e:
            print("Failed to process comment: " + str(e), file=sys.stderr)
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
            print('Analyzed %d comments, ' % i +
                  '%.2f%% too short/long, ' % percent_length_removed +
                  'found %d iambic pentameters ' % bot.n_pentameters_epoch +
                  '(total: %d), ' % bot.n_pentameters +
                  '%.1f comments/s' % (i / elapsed))
            sys.stdout.flush()
            # Sleep a bit
            time.sleep(bot.options.sleep_for)
            # Reset periodic counters
            bot.n_length_removed = 0
            bot.n_pentameters_epoch = 0
            i = 0
            start = time.time()
        # Occasionally tweet a quatrain
        try:
            bot.tweet_quatrain()
        except Exception, e:
            print("Failed to tweet " + str(e), file=sys.stderr)


def test():
    bot = RedditIambicPentameterBot(sys.argv[1])
    # Get reddit instance
    reddit = praw.Reddit(user_agent=bot.reddit.user_agent,
                         client_id=bot.reddit.client_id,
                         client_secret=bot.reddit.secret,
                         username=bot.reddit.user_name,
                         password=bot.reddit.password)
    # Get test comment
    test_comment = reddit.comment(id='cqmldc6')
    # Custom iambic pentameter
    test_comment.body = 'And cafeteria of other crackers'
    # Test
    bot.is_iambic_pentameter(test_comment, tweet=False)


if __name__ == '__main__':
    if '--test' in sys.argv:
        test()
    else:
        main()
