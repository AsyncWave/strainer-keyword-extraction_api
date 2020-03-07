import pandas as pd
import re
import Methods as m
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import CountVectorizer
spell = SpellChecker(distance = 1)

text_set = []
corpus = []# Final corpus

#read dataSet
print("reading dataset a")
dataSeta = pd.read_csv('venv/Data/corona.csv', names=['id', 'text'], header=1)
for text in dataSeta["text"]:
    text_set.append(text)
print("size of data" , len(text_set))
print("reading dataset b")
dataSetab = pd.read_csv('venv/Data/datar.csv', names=['id', 'text'], header=1)
for text in dataSetab["text"]:
    text_set.append(text)
print("size of data" , len(text_set))
print("reading dataset c")
dataSetac = pd.read_csv('venv/Data/fashion.csv', names=['id', 'text'], header=1)
for text in dataSetac["text"]:
    text_set.append(text)
print("size of data" , len(text_set))
print("reading dataset 1")
dataSet = pd.read_csv('venv/Data/Data.csv', names=['ID', 'TEXT'], header=1)
for text in dataSet["TEXT"]:
    text_set.append(text)
print("size of data" , len(text_set))
print("reading dataset 2")
dataSet2 = pd.read_csv('venv/Data/BuzzFeed_real_news_content.csv', names=['id','title','text','url','top_img','authors','source','publish_date','movies','images','canonical_link','meta_data'], header=1)
for text2 in dataSet2["text"]:
    text_set.append(text2)
print("size of data" , len(text_set))
print("Reading Dataset 3")
dataSet3 = open("venv/Data/HealthData.txt", "r")
for text3 in dataSet3:
    if text3.strip():
        text_set.append(text3)
dataSet3.close()
print("size of data" , len(text_set))
print("reading dataset 4")
dataSet = pd.read_csv('venv/Data/News_Category_Description.csv', names=['ID', 'short_description'], header=1)
for text4 in dataSet["short_description"]:
    text4 = str(text4)
    text_set.append(text4)
print("size of data", len(text_set))
print("reading dataset 5")
dataSet5 = pd.read_csv('venv/Data/helth2.csv', names=['ID', 'text'], header=1)
for text5 in dataSet5["text"]:
    text_set.append(text5)
print("size of data" , len(text_set))
print("reading dataset 6")
dataSet6 = pd.read_csv('venv/Data/news.csv', names= ['ID', 'text'], header=1)
for text6 in dataSet6["text"]:
    text_set.append(text6)
print("size of data" , len(text_set))
print("--text extraction done---")
print("saving collected data in to a file")
dataFrame = pd.DataFrame(text_set, columns=['text'])
dataFrame.to_csv('TextNotProcessedv2.csv')

print("--Defining Stop Words---")
# stop_words = set(stopwords.words("english"))
# new_words = ['omg', 'u', 'lol', 'gm', 'gn', 'gd9t', 'tc', 'rt', 'oops']
# stop_words = stop_words.union(new_words)

stop_words = m.read_stopwords()
print("data cleaning......")
for item in text_set:
    temporary_array = []
    item = str(item)
    item = re.sub(r"http\S+", "", item) #remove url
    item = re.sub('[^a-zA-Z]', ' ', item) #remove punctuations and numbers
    item = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", item) # greater than equal signs
    item = re.sub("(\\d|\\W)+", " ", item)#remove special characters
    item = item.lower() #convert to lower cases
    item = item.split()
    lem = WordNetLemmatizer()
    item = [lem.lemmatize(word) for word in item if not word in stop_words]
    item = " ".join(item)
    ps = PorterStemmer()
    tokenItem = word_tokenize(item)
    # ---Spelling correction--
    for word in tokenItem:
        nword = spell.correction(word)
        if word != nword:
            word = nword
        temporary_array.append(word)
     # ---//Spelling correction--

    corpus.append(TreebankWordDetokenizer().detokenize(temporary_array))

    # corpus.append(item)
print("corpus removing duplicates")
print("first", len(corpus))
corpus = list(dict.fromkeys(corpus))
# print(type(corpus))
# print(len(corpus))
print("corpus ready")

print('Start writing in to a file csv')
df = pd.DataFrame(corpus, columns=['text'])
df.to_csv('FinalCorpus.csv')
print('Everything is ready')
f = open("FinalCorpus.txt","w+")
for i in range(len(corpus)):
     f.write("%s\n" % corpus[i])
     # f.write("/n")
f.close()




