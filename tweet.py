import tweepy

def comment_to_tweet(comment):
    nsfw = '[NSFW] ' if comment.submission.over_18 else ''
    user = '/u/%s' % comment.author
    sub = '/r/%s' % comment.submission.subreddit
    text = comment.body
    return '%s From /u%s on %r:\n%s' % (nsfw, user, sub, text)

def tweet(text, twitter):
    auth = tweepy.OAuthHandler(twitter.consumer_key, twitter.consumer_secret)
    
    # Redirect user to Twitter to authorize
    redirect_user(auth.get_authorization_url())
    
    # Get access token
    auth.get_access_token(twitter.verifier_value)

    # Construct the API instance
    api = tweepy.API(auth)

    # Tweet
    api.update_status(text)

