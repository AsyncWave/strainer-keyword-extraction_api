import Methods as m
import Stanford
import  nltk
from nltk.tokenize import word_tokenize
import get_Old_Tweets_re as got
stop_words = m.read_stopwords()

ordering = []
nonordering = []
keystring = []
s = ''
# At least 80 "American terrorists" were killed in Iranian missile strikes on US targets in Iraq, Iranian state television claimed today.

# news_text = input("Please input news :")
# news_text = 'Pres. Trump’s tariffs and the retaliation by countries he has targeted have resulted in job losses and higher costs for U.S. manufacturers, a federal study recently found'
news_text = 'Regime special guard forces attacked citizens who were protesting peacefully. The crowd is calling the regime agents "dishonorable" Sunday January 12 #abc https://docs.google.com/document/d/1o_fvrKrCr61eDqXN6ak4UEqpBTpK0FPransm7FgwTOg/edit '
print("news", news_text)
tokenized_text = word_tokenize(news_text)

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
# print(tokenized_text)
# print(ordering)
# print(keywords)
for x in range(len(ordering)):
    s = s + ordering[x] + " "
    if len(s.split()) == 3:
        keystring.append(s)
        s = ''
    elif x == len(ordering)-1:
        keystring.append(s)
keystring = keystring + keywords
print("keystring", keystring)
#---Ordering the keywords---

# --- Calling Get)oldTweets---
got.getTweets(keystring)

# --- Calling Get)oldTweets---