import spacy
from .preprocessing import lemmatize_sentence

nlp = spacy.load('en_core_web_sm')

def check_for_expected_input(message, expected_inputs):
  """Checks whether a message an the expected input by checking ngrams
  of both the message and the expected inputs
  @param {String} message
  @param {List} expected_inputs
  @returns True if message is of expected inputs, else False."""
  lemmatized_message = lemmatize_sentence(message)
  doc = nlp(u"{}".format(lemmatized_message))
  for expected_input in expected_inputs:
    expected_input = nlp(u"{}".format(expected_input))
    input_length = len(expected_input)
    doc_length = len(doc)
    if doc_length == input_length:
      if lemmatized_message == expected_input.text:
        return True
    elif doc_length > input_length: 
      i = 0
      j = input_length
      while j <= doc_length:
        if doc[i:j].text == expected_input.text:
          return True
        i += 1
        j += 1
    else:
      i = 0
      j = doc_length
      while j <= input_length:
        if expected_input[i:j].text == doc.text:
          return True
        i += 1
        j += 1
  return False