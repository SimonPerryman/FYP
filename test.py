import os
import spacy
os.environ['APPLICATION_PATH'] = r"C:/dev/projects/university/FYP/"
from nlp_techniques import lemmatize_sentence
nlp = spacy.load("en_core_web_lg")

def check_for_crew(message):
  """Searches for crew members in the message using NER and then checks
  for keywords which a crew member's name would be expected to be followed by.
  @param {String} message
  @returns {List} crew names"""
  crew = set()
  crew_present = False
  doc = nlp(u'{}'.format(message))
  docLower = nlp(u'{}'.format(message.lower()))
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      crew.add(ent.text)
    
  for token in docLower:
    if token.text == "with" or token.text == "starring":
      message = message[token.idx:].title()
      crew_present = True
    
    if token.text == "by":
      for anc in token.ancestors:
        if anc.text == "directed" or anc.text == "written":
          message = message[token.idx:].title()
          crew_present = True
  print(message)
  # if crew_present:
  #   doc = nlp(message)
  #   for child in doc[0].children:
  #     if child.pos_ == "NOUN" or child.pos_ == "PROPN":


  return list(crew)

def test():
  check_for_crew("Suggest a film directed by Tom Cruise and Bruce Willis")
  check_for_crew("Suggest a film starring Tom Cruise and Bruce Willis")
  # doc = nlp(u"I really enjoy films about SpiderMan and Superman")

  # for ent in doc.ents:
  #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

  return True

if __name__ == '__main__':
  test()
