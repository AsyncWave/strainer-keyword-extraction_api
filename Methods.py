import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

# read Stopwords
def read_stopwords():
    fp = open("data/SmartStoplist.txt", "r")
    stopwordss = []
    words = fp.readlines()
    for word in words:
        word = re.sub(r"\n","",word)
        stopwordss.append(word)
    stopwordss = set(stopwordss)
    new_words = ['omg', 'u', 'lol', 'gm', 'gn', 'gd9t', 'tc', 'rt', 'oops','ok']
    stopwordss = stopwordss.union(new_words)
    stop_words = set(stopwords.words("english"))
    stopwordss = stopwordss.union(stop_words)
    return stopwordss


def text_cleaning(text,stop_words):
    text = re.sub(r"http\S+", "", text)  # remove url
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)  # greater than equal signs
    text = re.sub("(\\d|\\W)+", " ", text)  # remove special characters
    return text

def test_data_cleaning(text):
    text = re.sub(r"http\S+", "", text)  # remove url
    text = re.sub(r"@\S+", "", text)  # remove url
    text = re.sub(r"RT","",text)
    text = re.sub(r"#\S+", "", text)
    return text