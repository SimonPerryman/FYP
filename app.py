import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
# nltk.download()
# nltk.download('state_union')
# nltk.download('punkt')
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
#
# def process_content():
#     try:
#         for i in tokenized[5:]:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#
#             namedEnt = nltk.ne_chunk(tagged, binary=True)
#             namedEnt.draw()
#
#     except Exception as e:
#         print(str(e))
#
#
# process_content()

sentences = ["Suggest a film for me!", "What is a good film to watch at the moment", "Give me a Steven Spielberg movie",
             "Show me a song that steven spielberg directed that i have not seen yet", "any film", "film",
             "please can you suggest a comedy", "how are you doing today", "hello", "shut up", "go away",
             "suggest a tv show for me please", "Thanks for that, can you suggest another film",
             "I've seen that one before. Give me another suggestion", "What do you think of The Greatest Showman",
             "Is Frozen a good film"]

# Lemmatizer
# Sentiment Analysis
# Morphology
# Tokenize
lemmatizer = WordNetLemmatizer()
lemmatizedNormal = []
lemmatizedLower = []
POSNormal = []
POSNormalLemma = []
POSLower = []
POSLowerLemma = []

for sentence in sentences:
    words = word_tokenize(sentence)
    POSNormal.append(pos_tag(words))
    lemmaWords = []
    for word in words:
        lemmaWords.append(lemmatizer.lemmatize(word))
    lemmatizedNormal.append(lemmaWords)
    temp = " ".join(lemmaWords)
    print(temp)
    print(pos_tag(temp))

    # Lowercase all
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    POSLower = pos_tag(words)
    lemmaWords = []
    for word in words:
        lemmaWords.append(lemmatizer.lemmatize(word))
    lemmatizedLower.append(lemmaWords)
    POSNormalLemma = pos_tag(" ".join(lemmaWords))


print("LemmatizedNormal", lemmatizedNormal)
print("LemmatizedLower", lemmatizedLower)
print("POSNormal", POSNormal)
print("POSNormalLemma", POSNormalLemma)
print("POSNLower", POSLower)
print("POSNLowerLemma", POSLowerLemma)
