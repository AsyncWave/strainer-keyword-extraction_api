import Methods as m
import Stanford
import pandas as pd
import re
# import main

# stop_words = m.read_stopwords()


test_set = pd.read_csv('venv/Data/TestSet3 v7.csv', names=['ID', 'text', 'keywords', 'Person', 'Location', 'Date', 'Organization', 'Nouns', 'Verbs', 'Synonyms'], header=1)
print(len(test_set))
print(type(test_set))
keyword =[]
text = []
for record in test_set['keywords']:
    record = str(record)
    record = re.sub(r"\n", "", record)
    l = record.split(",")
    keyword.append(l)

for txt in test_set['text']:
    txt = str(txt)
    text.append(txt)


print (text[1])
#
# for x in range(99):
#
#     candidate_keywords = Stanford.extract_candidate_keywords(text[x])
#     candidate_keywords = [m.lower() for m in candidate_keywords]
#
#     keywords = list(dict.fromkeys(candidate_keywords))  # remove duplicates
#     print(keywords)
#     print(text[x], keyword[x])