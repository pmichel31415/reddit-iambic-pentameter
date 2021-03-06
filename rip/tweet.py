# -*- coding: utf-8 -*-
import tweepy


def comment_to_tweet(comment):
    """Makes a tweet from a comment (with author/subreddit/nsfw tag)"""
    # Mark if the comment is from a NSFW post just in case
    nsfw = '[NSFW] ' if comment.submission.over_18 else ''
    user = '/u/%s' % comment.author
    sub = '/r/%s' % comment.submission.subreddit
    text = comment.body.strip()
    tweet = '%s "%s"\n\n(from %s in %s)' % (nsfw, text, user, sub)
    return tweet


def authenticate(twitter):
    """Authenticate and return a twitter api object"""
    # Create the OAuth instance
    auth = tweepy.OAuthHandler(twitter.consumer_key, twitter.consumer_secret)
    # Get access token
    auth.set_access_token(twitter.access_token, twitter.access_token_secret)
    # Construct the API instance
    return tweepy.API(auth)


def tweet(text, twitter):
    """Sends a tweet with the given text"""
    api = authenticate(twitter)
    # Cut text to 140 characters if needed
    if len(text) > 140:
        text = text[:139] + '…'
    # Tweet
    api.update_status(text)


def tweet_image(source, twitter, text=''):
    """Sends a tweet with the given text"""
    api = authenticate(twitter)
    # Tweet
    api.update_with_media(source, text)
