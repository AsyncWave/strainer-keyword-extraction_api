from pycorenlp import StanfordCoreNLP
import wordFreq as wf
import SynonymTest as syn


def extract_candidate_keywords(text):
    nouns = []
    organization = []
    title = []
    person = []
    date = []
    country = []
    verbs = []
    city = []
    nationality = []
    candidateKeywords = []
    forTFIDF = []
    nlp_wrapper = StanfordCoreNLP(' http://192.248.15.148:9000')
    # nlp_wrapper = StanfordCoreNLP('https://strainer-stanford-core.azurewebsites.net')
    doc = text
    annot_doc = nlp_wrapper.annotate(doc,
        properties={
            'annotators': 'ner, pos',
            'outputFormat': 'json',
            'timeout': 100000,
        })
    # print("annotated ", annot_doc)
    #
    for sentence in annot_doc["sentences"]:
        for word in sentence["tokens"]:
            # print(word["word"] + " => " + word["ner"] + " => " + word["pos"])
            if word["ner"] == "O":
                if word["pos"] == "NN" or word["pos"] == "NNP" or word["pos"] == "NNPS" or word["pos"] == "NNS":
                    nouns.append(word["word"])
                if word["pos"] == "VBG" or word["pos"] == "VBD" or word["pos"] == "VBN" or word["pos"] == "VBP" or\
                        word["pos"] == "VB":
                    verbs.append(word["lemma"])
            if word["ner"] == "TITLE":
                title.append(word["word"])
            if word["ner"] == "ORGANIZATION":
                organization.append(word["word"])
            if word["ner"] == "COUNTRY":
                country.append(word["word"])
            if word["ner"] == "PERSON":
                person.append(word["word"])
            if word["ner"] == "NATIONALITY":
                nationality.append(word["word"])
            if word["ner"] == "CITY":
                city.append(word["word"])
            if word["ner"] == "DATE":
                date.append(word["word"])
    if len(nouns) != 0:
        print("Nouns",nouns)
    if len(person) != 0:
        print("Person", person)
    if len(organization) != 0:
        print("Organization", organization)
    if len(country) != 0:
        print("Country", country)
    if len(title) != 0:
        print("Title", title)
    if len(verbs) != 0:
        print("Verbs", verbs)
    if len(city) != 0:
        print("City", city)
    if len(nationality) != 0:
        print("Nationality", nationality)
    if len(date) != 0:
        print("date", date)
    if len(date)!= 0:
        strn = ' '.join(date)
        date = []
        date.append(strn)


    joinedlist =  organization + country + title + city + nationality + person + date + nouns


    # print (joinedlist)
    check_tfIdf = " ".join(verbs)
    tf = wf.take_word_frequency(check_tfIdf)
    forTFIDF = tf + nouns
    for key in forTFIDF:
        words = syn.get_syn_words(key)
        candidateKeywords = candidateKeywords + words
    # print("candidate keywords ", candidateKeywords + joinedlist)
    return candidateKeywords + joinedlist

# extract_candidate_keywords('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')