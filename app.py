# import nltk
from nltk.tokenize import word_tokenize

import questions
import text_processing as tp
from nltk.corpus import wordnet

#Synsets & WordNets


synsets = wordnet.synsets("Suggest")

print(synsets)

#synset
print(synsets[0].name())

# just the word
print(synsets[0].lemmas()[0].name())

# definition
print(synsets[0].definition())

#examples
print(synsets[0].examples())



# def synsets_calc(synsets):
#     synonyms = []
#     antonyms = []
#     for syn in synsets:
#         for l in syn.lemmas():
#             synonyms.append(l.name())
#             if l.antonyms():
#                 antonyms.append(l.antonyms()[0].name())
#     return {
#         'selfWord': synsets,
#         'synonyms': synonyms,
#         'antonyms': antonyms
#     }
# print(synsets_calc("What"))

# print(wordnet.synsets("What"))
# InputWord = wordnet.synsets(word_tokenize(questions.sentences[1])[0])
# print(word_tokenize(questions.sentences[1])[0])

# print(InputWord)
abc = tp.get_synsets("Starving")
# print(abc['synonyms'])
# synsets_calc("Better")
