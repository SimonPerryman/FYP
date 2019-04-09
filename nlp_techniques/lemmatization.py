import spacy
nlp = spacy.load('en_core_web_lg')

def lemmatize_sentence(sentence):
  """Returns a lemmatized version of a sentence
  @param {String} sentence
  @returns {String} lemmatized sentence"""
  doc = nlp(u"{}".format(sentence.lower()))
  return ' '.join([token.lemma_ for token in doc])