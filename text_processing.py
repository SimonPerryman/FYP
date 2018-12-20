import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

def convert_pos(pos):
    #TODO: Implement Adjective Satellites - i.e. collocations (e.g. red wine)
    if(re.match(r'VB.', pos)):
        pos = 'VB'
    elif(re.match(r'JJ.', pos)):
        pos = 'JJ'
    elif(re.match(r'RB.', pos)):
        pos = 'RB'
     # No need to check for a noun as that is the default
    return {
        'JJ': 'a',
        'ADV': 'a',
        'RB': 'r',
        'VB': 'v'
    }.get(pos, 'n')


def get_synsets(word):
    synsets = wordnet.synsets(word)
    synonyms = []
    antonyms = []
    for syn in synsets:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return {
        'selfWord': word,
        'synsets': synsets,
        'synonyms': set(synonyms),
        'antonyms': set(antonyms)
    }


def lemmatization_testing(lower, sentences):
    lemmatizer = WordNetLemmatizer()
    file = open("Textprocessing.txt", "w")
    if lower == 1:
        sentences = sentences.lower()
        dataType = "LOWER"
    else:
        dataType = "UPPER"
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        file.write("{0} POS_TAG: {1}\n".format(dataType, tagged))
        lemmaWords = []
        for i in range(0, len(words)):
            lemmaWords.append(lemmatizer.lemmatize(words[i], pos=convert_pos(tagged[i][1])))
        file.write("{0} Lemmatized: {1}\n".format(dataType, lemmaWords))
        file.write("{0} POS_TAG Lemmatized: {1}\n".format(dataType, pos_tag(word_tokenize(" ".join(lemmaWords)))))
        file.write("\n")
    file.close()

def get_synsets(word):
    synsets = wordnet.synsets(word)
    synonyms = []
    antonyms = []
    for syn in synsets:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return {
        'selfWord': word,
        'synsets': synsets,
        'synonyms': set(synonyms),
        'antonyms': set(antonyms)
    }

# def processing_comparisons(sentences):
#     lemmatizer = WordNetLemmatizer()
#     lemmatizedNormal = []
#     lemmatizedLower = []
#     POSNormal = []
#     POSNormalLemma = []
#     POSLower = []
#     POSLowerLemma = []

#     file = open("Textprocessing.txt", "w")

#     for sentence in sentences:
#         words = word_tokenize(sentence)
#         tagged = pos_tag(words)
#         print("Normal POS_TAG:", tagged)
#         file.write("Normal POS_TAG: {0}\n".format(tagged))
#         # POSNormal.append(tagged)
#         lemmaWords = []
#         for i in range(0, len(words)):
#             lemmaWords.append(lemmatizer.lemmatize(words[i], pos=convert_pos(tagged[i][1])))
#         print("Normal Lemmatized", lemmaWords)
#         file.write("Normal Lemmatized: {0}\n".format(lemmaWords))
#         print("Normal POS_TAG Lemmatized:", pos_tag(word_tokenize(" ".join(lemmaWords))))
#         file.write("Normal POS_TAG Lemmatized: {0}\n".format(pos_tag(word_tokenize(" ".join(lemmaWords)))))
#         lemmatizedNormal.append(lemmaWords)
#         # POSNormalLemma.append(pos_tag(word_tokenize(" ".join(lemmaWords))))

#         # Lowercase all
#         sentence = sentence.lower()
#         words = word_tokenize(sentence)
#         tagged = pos_tag(words)
#         # print("Lower Tokenized:", words)
#         print("Lower POS_TAG:", tagged)
#         file.write("Normal POS_TAG: {0}\n".format(tagged))
#         POSLower = pos_tag(words)
#         lemmaWords = []
#         for i in range(0, len(words)):
#             lemmaWords.append(lemmatizer.lemmatize(words[i], pos=convert_pos(tagged[i][1])))
#         print("Lower Lemmatized", lemmaWords)
#         file.write("Lower Lemmatized: {0}\n".format(lemmaWords))
#         print("Lower POS_TAG Lemmatized:", pos_tag(word_tokenize(" ".join(lemmaWords))))
#         file.write("Lower POS_TAG Lemmatized: {0}\n".format(pos_tag(word_tokenize(" ".join(lemmaWords)))))
#         lemmatizedLower.append(lemmaWords)
#         POSLowerLemma.append(pos_tag(word_tokenize(" ".join(lemmaWords))))

#         print("\n\n")
#         file.write("\n\n")

#         file.close()