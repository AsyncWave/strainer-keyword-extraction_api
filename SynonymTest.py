from nltk.corpus import wordnet
import spacy
nlp = spacy.load("en_core_web_sm")


# synonims by nltk corpus
def get_syn_words(item):
    word = item
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    # print("synonym for " , word)
    synonym = set(synonyms)
    # for s in synonym:
    #     print(s)
    similer_words = check_similarity(synonym, word)
    return similer_words
# //synonims by nltk corpus


def check_similarity(wordtest, check_word):
    similar_words = []
    try:
        token1 = nlp(check_word)
        for word in wordtest:
            token2 = nlp(word)
            if token2.has_vector == True and token1.similarity(token2) > 0.65 and token1.similarity(token2) < 1:
                # print("Similarity:", token1.similarity(token2), word, token2.has_vector)
                similar_words.append(word)
        return similar_words
    except BaseException as e:
        print("Error on_data: %s" % str(e))
