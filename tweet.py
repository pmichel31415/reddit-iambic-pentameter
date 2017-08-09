# -*- coding: utf-8 -*-
import tweepy
import sys

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def comment_to_tweet(comment):
    nsfw = '[NSFW] ' if comment.submission.over_18 else ''
    user = '/u/%s' % comment.author
    sub = '/r/%s' % comment.submission.subreddit
    text = comment.body
    tweet = '%s "%s"\n\n(from %s in %s)' % (nsfw, text, user, sub)
    if len(tweet) > 140:
        tweet = tweet[:139] + '…'
    return tweet

def tweet(text, twitter):
    auth = tweepy.OAuthHandler(twitter.consumer_key, twitter.consumer_secret)
    
    # Get access token
    auth.set_access_token(twitter.access_token, twitter.access_token_secret)

    # Construct the API instance
    api = tweepy.API(auth)

    # Tweet
    api.update_status(text)

