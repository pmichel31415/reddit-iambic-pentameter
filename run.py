# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time

from rip import RedditIambicPentameterBot


def main_loop(bot):
    """Main loop for the bot"""
    # Start looping
    i = 0
    bot.tick()
    for comment in bot.r_all.stream.comments():
        # Check if comment is and iambic pentameter
        done = bot.process_comment(comment)
        # If enough commebts have been processed, kill the procgram
        if done:
            exit()
        # Increment counter
        i += 1
        # Report periodically
        if i >= bot.options.report_every:
            # Print infos
            percent_length_removed = (bot.n_length_removed) / bot.options.report_every * 100
            print('Analyzed %d comments, ' % i +
                  '%.2f%% too short/long, ' % percent_length_removed +
                  'found %d iambic pentameters ' % bot.n_pentameters_epoch +
                  '(total: %d), ' % bot.n_pentameters +
                  '%.1f comments/s' % (i / bot.tick()))
            sys.stdout.flush()
            # Sleep a bit
            time.sleep(bot.options.sleep_for)            # Reset periodic counters
            # Reset periodic counters
            bot.n_length_removed = 0
            bot.n_pentameters_epoch = 0
            i = 0
        # Occasionally tweet a quatrain
        try:
            bot.tweet_quatrain()
        except Exception as e:
            print("Failed to tweet " + str(e), file=sys.stderr)


def main():
    # Instantiate bot
    bot = RedditIambicPentameterBot(sys.argv[1])
    # Run in while loop to recover from unknown exceptions
    while True:
        try:
            # Run main loop            main_loop(bot, subreddit)
            main_loop(bot)
        except Exception as e:
            print('Unknown error: ' + str(e), file=sys.stderr)


def test():
    bot = RedditIambicPentameterBot(sys.argv[1])
    # Get test comment
    test_comment = bot.r.comment(id='cqmldc6')
    # Custom iambic pentameter
    test_comment.body = 'And cafeteria of other crackers'
    # Test
    bot.is_iambic_pentameter(test_comment, tweet=False)


if __name__ == '__main__':
    if '--test' in sys.argv:
        test()
    else:
        main()
