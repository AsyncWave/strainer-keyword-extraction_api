import Methods as m
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
# stop_words = set(m.read_stopwords())

stop_words = set(stopwords.words("english"))
new_words = ['omg','lol', 'gm', 'gn', 'gd9t', 'tc','rt','oops']
stop_words = stop_words.union(new_words)

corpus = []
#---Read the text file---
f = open("FinalCorpus.txt", "r")
if f.mode != 'r':
    print("File mode is not read ")
    f = open("newCorpus.txt", "r")
f1 = f.readlines()
for line in f1:
    corpus.append(line)

# dataSet = pd.read_csv('FinalCorpus.csv', names=['id', 'text'], header=1)
# for text in dataSet["text"]:
#     corpus.append(text)
# print("corpus read")


def take_word_frequency(text):
    cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
    X=cv.fit_transform(corpus)

    text = text
    tfidf_keys = []
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    # get feature names
    feature_names = cv.get_feature_names()

    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([text]))

    # Function for sorting tf_idf in descending order
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)

    for k in keywords:
        if keywords[k] >= 0.5:
            # print(k, keywords[k])
            tfidf_keys.append(k)

    return tfidf_keys

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


# sort the tf-idf vectors by descending order of scores
