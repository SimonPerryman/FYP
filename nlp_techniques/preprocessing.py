import spacy
nlp = spacy.load('en_core_web_lg')

def lemmatize_sentence(sentence):
  """Returns a lemmatized version of a sentence
  @param {String} sentence
  @returns {String} lemmatized sentence"""
  doc = nlp(u"{}".format(sentence.lower()))
  return ' '.join([token.lemma_ for token in doc])

def preprocess_reviews(review):
    """Preprocesses reviews, removing all stopwords, punctuations and singular letter words
    @param {List} Review
    @returns {String} preprocessed Review
    """
    processed_review = []
    for word in review:
        doc = nlp(word)[0]
        if not doc.is_stop and not doc.is_punct and len(doc) > 1:
            processed_review.append(doc.text)
    return lemmatize_sentence(" ".join(processed_review))