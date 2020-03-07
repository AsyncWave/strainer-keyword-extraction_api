import numpy as np
import pickle
import hashlib
import json
import re
import tweepy
import requests
import traceback
import GetOldTweets3 as got
from datetime import datetime, timedelta
import pandas as pd

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import Methods as m
import Stanford

from nltk.tokenize import word_tokenize
# import get_Old_Tweets_re as got
stop_words = m.read_stopwords()

from werkzeug.wsgi import ClosingIterator
from flask_sqlalchemy import SQLAlchemy
from bson import json_util
from flask import Flask, request, jsonify, render_template, abort, Response
from flask_pymongo import PyMongo 
from flask_cors import CORS, cross_origin
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

mongo = PyMongo()

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

CORS(app)

consumer_key = 'ZZaq1WNWyrct8TC6KhBHPZg3F'
consumer_secret_key = 'DAVIqeOOw0iU9r3zczCD9BJcykyGTbccetw67KOZ3rPzXM3t8v'
access_token = '376020588-fPbhUUYEVvfrHHwjvKth0fkInHKjIwa2pbIl8HNJ'
access_token_secret = 'vHZyi5tWus8UgXICtWrz82em1Dv9R2eS8wQ398jMreJMM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
max_tweets = 1000

query_Id = 0


class AfterThisResponse:
    def __init__(self, app=None):
        self.callbacks = []
        if app:
            self.init_app(app)

    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback

    def init_app(self, app):
        # install extensioe
        app.after_this_response = self

        # install middleware
        app.wsgi_app = AfterThisResponseMiddleware(app.wsgi_app, self)

    def flush(self):
        try:
            for fn in self.callbacks:
                try:
                    fn()
                except Exception:
                    traceback.print_exc()
        finally:
            self.callbacks = []

class AfterThisResponseMiddleware:
    def __init__(self, application, after_this_response_ext):
        self.application = application
        self.after_this_response_ext = after_this_response_ext

    def __call__(self, environ, start_response):
        iterator = self.application(environ, start_response)
        try:
            return ClosingIterator(iterator, [self.after_this_response_ext.flush])
        except Exception:
            traceback.print_exc()
            return iterator

class Tweet(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    queryId = db.Column(db.Integer)
    tweet = db.Column(db.Text)
    in_reply_to_status_id = db.Column(db.Text)
    screen_name = db.Column(db.Text)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.Text)
    lang = db.Column(db.Text)
    status = db.Column(db.Text)
    has_extended_profile = db.Column(db.Boolean)
    name = db.Column(db.Text)
    created_at = db.Column(db.Text)
    verified = db.Column(db.Boolean)
    followers_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    statuses_count = db.Column(db.Integer)
    listed_count = db.Column(db.Integer)
    favourites_count = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    geo = db.Column(db.Text)
    tweetid = db.Column(db.Text)
    retweets = db.Column(db.Integer)
    record_created_at = db.Column(db.DateTime, default = datetime.now)

AfterThisResponse(app)

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
@cross_origin()
def query():
    global query_Id
    global news_text
    data = request.get_json(force=True)
    if not data or not 'queryId' in data:
        abort(400)

    query_Id = data['queryId']
    news_text = data['query']
    # keyword_list = data['keyword_list']
    # print('keyword_list <<<<', keyword_list)
    print('data <<<<', data)

    # background process
    @app.after_this_response
    def post_process():
        # Extract Keywoords here using 'tweet'
        # ----------------------------------
        global news_text
        ordering = []
        nonordering = []
        keystring = []
        s = ''
        data_set = []

        tokenized_text = word_tokenize(news_text)
        # tokenized_text = word_tokenize(user_text)
        news_text = str(m.text_cleaning(news_text, stop_words))
        #----getting keywords ----
        candidate_keywords = Stanford.extract_candidate_keywords(news_text)
        candidate_keywords = [m.lower() for m in candidate_keywords]
        keywords = list(dict.fromkeys(candidate_keywords))#remove duplicates
        print("keywords", keywords)
        #----getting keywords---

        #---Ordering the keywords---
        for word in tokenized_text:
            for kword in keywords:
                if word.lower() == kword:
                    ordering.append(kword)
                    keywords.remove(kword)

        ordering = ordering + keywords
        for x in range(len(ordering)):
            s = s + ordering[x] + " "
            if len(s.split()) == 3:
                keystring.append(s)
                s = ''
            elif x == len(ordering)-1:
                keystring.append(s)
        print("keystring", keystring)
        # keystring = keystring + keywords

        keyword_list = keystring

        # news_text = tweet_text #'Regime special guard forces attacked citizens who were protesting peacefully. The crowd is calling the regime agents "dishonorable" Sunday January 12 #abc https://docs.google.com/document/d/1o_fvrKrCr61eDqXN6ak4UEqpBTpK0FPransm7FgwTOg/edit '
        print("news >>>", news_text)
        print("keyword_list >>>", keyword_list)
        # tokenized_text = word_tokenize(news_text)

        querySearchTerm = ''
        endDate = datetime.today().strftime('%Y-%m-%d')
        startDate = (datetime.today() - timedelta(days = 2000)).strftime('%Y-%m-%d')
        global counter
        tweetLimit = 5
        count = 1

        try:
            for elem in keyword_list:
                querySearchTerm = elem
                print("querySearchTerm", querySearchTerm)
                tweetCriteria = got.manager.TweetCriteria().setQuerySearch(querySearchTerm) \
                    .setSince(startDate) \
                    .setUntil(endDate) \
                    .setMaxTweets(tweetLimit)

                for index, x in enumerate(got.manager.TweetManager.getTweets(tweetCriteria)):
                    datestring = str(x.date)

                    # user_data_tweepy = get_data_tweepy(x.username, x.id)

                    consumer_key = 'vfbYJnzktYxk75Au9F4zyzBJJ'
                    consumer_secret_key = 'Vj5R6QzuZAbPAJKe8fIAmOBsHspmUSoGZDevuA7VZf81y2bnJK'
                    access_token = '4834192821-iVslQFIReWAegd0TDKyZGHNm9zik1gSjgqCAXmF'
                    access_token_secret = 'mF7xsBn27IxXa4raDwJzVzK5ey8oPLqtuTrv4oj8lYhuR'
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
                    auth.set_access_token(access_token, access_token_secret)
                    api = tweepy.API(auth)

                    user_data_tweepy = api.get_user(x.username)
                    status = api.get_status(x.id)
                    # user.in_reply_to_status_id_str = status.in_reply_to_status_id_str
                    # tweet = api.get_status(1232781683885314056)
                    # print(tweet.in_reply_to_status_id_str)
                    tweet = Tweet()

                    tweet.queryId = query_Id
                    tweet.tweetid = str(x.id)
                    tweet.retweets = str(x.retweets)
                    tweet.tweet = x.text
                    tweet.in_reply_to_status_id_str = status.in_reply_to_status_id_str
                    tweet.screen_name = str(user_data_tweepy.screen_name)
                    tweet.location = str(user_data_tweepy.location)
                    tweet.description = str(user_data_tweepy.description)
                    tweet.url = str(user_data_tweepy.url)
                    tweet.lang = str(user_data_tweepy.lang)
                    tweet.status = x.text
                    tweet.has_extended_profile = user_data_tweepy.default_profile_image
                    tweet.name = str(user_data_tweepy.name)
                    tweet.created_at = str(user_data_tweepy.created_at)
                    tweet.verified = user_data_tweepy.verified
                    tweet.followers_count = user_data_tweepy.followers_count
                    tweet.friends_count = user_data_tweepy.friends_count
                    tweet.statuses_count = user_data_tweepy.statuses_count
                    tweet.listed_count = user_data_tweepy.listed_count
                    tweet.favourites_count = user_data_tweepy.favourites_count
                    tweet.favorites = str(x.favorites)
                    tweet.geo = str(x.geo)

                    db.session.add(tweet)
                    db.session.commit()

                    print("Tweet " + str(count) + " collected")
                    count += 1
                    # user_data_tweepy = get_data_tweepy(x.username)
                    # type = datestring + ' | ' + str(x.id) + ' | ' + str(x.username) + ' | ' + x.text + ' | ' + str(x.retweets) + \
                    #     ' | ' + str(x.favorites) + ' | '+ str(x.geo) + user_data_tweepy
                    # print(type)
                    # data_set.append(type)
                print("Done for ", elem)
        except Exception:
            traceback.print_exc()
            print("Something went wrong")
        finally:
            r = requests.post('https://strainer-rest-api.herokuapp.com/setdata/'+str(query_Id))
            print(r)
            # r = requests.post('https://strainer-forecast.herokuapp.com/setdata/'+str(query_Id))
            # print(r)
            # write_file(data_set)

    return jsonify({'queryId': data['queryId'],'message': 'Data collection initiated'}), 201

@app.route('/get/<id>', methods=['GET'])
@cross_origin()
def get(id):
    try:
        queryId = int(id)
    except:
        return jsonify({'message': 'Not a valid Id'}), 400
    
    tweets = Tweet.query.filter_by(queryId=id).all()
    if tweets == []:
        return jsonify({'queryId': queryId, 'message': 'Nothing is available for Id ' + id + ', rechek and try again!'}), 400
    json_results = [t.to_dict() for t in tweets]
    return jsonify(json_results), 200

if __name__ == "__main__":
    app.run(debug=True)