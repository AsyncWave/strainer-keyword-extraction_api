import GetOldTweets3 as got
from datetime import datetime, timedelta
import tweepy
import json
import pandas as pd
import traceback
data_set = []

def get_data_tweepy(user_name):
    # print("tweepy called ")
    consumer_key = 'vfbYJnzktYxk75Au9F4zyzBJJ'
    consumer_secret_key = 'Vj5R6QzuZAbPAJKe8fIAmOBsHspmUSoGZDevuA7VZf81y2bnJK'
    access_token = '4834192821-iVslQFIReWAegd0TDKyZGHNm9zik1gSjgqCAXmF'
    access_token_secret = 'mF7xsBn27IxXa4raDwJzVzK5ey8oPLqtuTrv4oj8lYhuR'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.get_user(user_name)
    # u_data = str(user.screen_name) + ' | ' + str(user.created_at) + ' | ' + str(user.followers_count) + ' | ' + \
    #          str(user.verified) + ' | ' + str(user.listed_count) + ' | ' + str(user.default_profile) + ' | ' + \
    #          str(user.statuses_count) + ' | ' + str(user.friends_count) + ' | ' + str(user.favourites_count) + ' | ' +\
    #          str(user.location) + ' | ' + str(user.description) + ' | ' +  str(user.url) + ' | ' + str(user.lang)
    # return u_data
    return user

def getTweets(keyword_list):

    querySearchTerm = ''
    endDate = datetime.today().strftime('%Y-%m-%d')
    startDate = (datetime.today() - timedelta(days = 2000)).strftime('%Y-%m-%d')
    operator = 'or'
    for i in range(len(keyword_list)):
        if i != len(keyword_list)-1:
            querySearchTerm = querySearchTerm + " '" + keyword_list[i] + "' " + operator
        else:
            querySearchTerm = querySearchTerm + " '" + keyword_list[i] + "' "
    #querySearchTerm = ' \'regime guard forces \' OR \'citizens crowd agents \' OR \'force\' OR \'citizen\' OR \'agent\' OR \'sunday january 12\''
    querySearchTerm ='citizens crowd agents'
    print("q4", querySearchTerm)
    global counter
    tweetLimit = 10
    try:
        print("q", querySearchTerm)
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(querySearchTerm) \
            .setSince(startDate) \
            .setUntil(endDate) \
            .setMaxTweets(tweetLimit)
        print(tweetCriteria)
        # obj = got.manager.TweetManager.getTweets(tweetCriteria)
        # print(obj)
        for index, x in enumerate(got.manager.TweetManager.getTweets(tweetCriteria)):
            datestring = str(x.date)
            user_data_tweepy = get_data_tweepy(x.username)
            tweet = Tweet()

            tweetid = str(x.id)
            retweets = str(x.retweets)
            tweet.text = x.text
            tweet.screen_name = str(user_data_tweepy.screen_name)
            tweet.location = str(user_data_tweepy.location)
            tweet.description = str(user_data_tweepy.description)
            tweet.url = str(user_data_tweepy.url)
            tweet.lang = str(user.lang)
            tweet.status = x.text
            tweet.has_extended_profile = user_data_tweepy.default_profile_image
            tweet.name = str(user_data_tweepy.name)
            tweet.created_at = str(user_data_tweepy.created_at)
            tweet.verified = user_data_tweepy.verified
            tweet.followers_count = user_data_tweepy.followers_count
            tweet.friends_count = user_data_tweepy.friends_count
            tweet.statuses_count = user_data_tweepy.statuses_count
            tweet.listed_count = user_data_tweepy.listed_count
            favourites_count = user_data_tweepy.favourites_count
            favorites = str(x.favorites)
            geo = str(x.geo)

            # type = datestring + ' | ' + str(x.id) + ' | ' + str(x.username) + ' | ' + x.text + ' | ' + str(x.retweets) + \
            #        ' | ' + str(x.favorites) + ' | '+ str(x.geo) + user_data_tweepy
            # obj = x + user_data_tweepy
            # print(type)
            data_set.append(tweet)
            
    except Exception:
        traceback.print_exc()
        print("Something went wrong")
    finally:
        return data_set
        # write_file(data_set)


def write_file(data_list):
    print("Started writing file")

    f = open("collected_tweets4.txt", "w+", encoding="utf-8")
    f.write("date | id | username | text | retweets | favorites | geo | screen_name | created_at | followers_count |"
            " verified | listed_count | default_profile | statuses_count | friends_count | favorites_count | location "
            "| description | url | lang\n")
    for i in range(len(data_list)):
        record = str(data_list[i])
        f.write("%s\n" % record)
    f.close()

# keystring =  ['regime guard forces ', 'citizens crowd agents ', 'force', 'citizen', 'agent', 'sunday january 12']
# getTweets(keystring)