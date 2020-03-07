import pandas as pd
from nltk.corpus import twitter_samples

# print(twitter_samples.fileids())
preData_set =[]
#getting data
tweet_set = twitter_samples.strings("tweets.20150430-223406.json")
for tweet in tweet_set:
    preData_set.append(tweet)
print("tweets were appended" )
print(len(preData_set))

df = pd.DataFrame(preData_set)
df.to_csv('Data.csv')


