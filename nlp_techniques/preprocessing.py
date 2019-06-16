"""

Text preprcoessing functions file

Review preprocessing has the option of keeping stopwords and removing them

"""

import re
import spacy
nlp = spacy.load('en_core_web_sm')

def lemmatize_sentence(sentence):
  """Returns a lemmatized version of a sentence
  @param {String} sentence
  @returns {String} lemmatized sentence"""
  doc = nlp(u"{}".format(sentence.lower()))
  return ' '.join([token.lemma_ for token in doc])

def preprocess_string(string):
    """Removes all a lowercase string with all characters which are not a word, digit or whitespace
    are removed.
    @param {String} string
    @returns {String} preprocessed string"""
    return re.sub(r"[^\d^\w]", "", string.lower())

def preprocess_reviews(review):
    """Preprocesses reviews, removing all stopwords, digits, punctuations and singular letter words
    @param {List} Review
    @returns {String} preprocessed Review
    """
    processed_review = []
    for word in review:
        doc = nlp(word)[0]
        if not doc.is_stop and not doc.is_punct and len(doc) > 1 and not doc.is_digit:
            processed_review.append(doc.text)
    return lemmatize_sentence(" ".join(processed_review))

def preprocess_reviews_keep_stop_words(review):
    """Preprocesses reviews, removing all digits, punctuations and singular letter words
    @param {List} Review
    @returns {String} preprocessed Review
    """
    processed_review = []
    for word in review:
        doc = nlp(word)[0]
        if not doc.is_punct and len(doc) > 1 and not doc.is_digit:
            processed_review.append(doc.text)
    return lemmatize_sentence(" ".join(processed_review))