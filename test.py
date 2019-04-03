import spacy
nlp = spacy.load('en_core_web_lg')
from database import getCrewBySimilarName
# import sys
# sys.path.insert(0, 'C:/dev/projects/University/FYP/recommendation-system/')
# import pandas as pd
import numpy as np
from spacy import displacy

# from create_table import getFilmTable
# from sklearn.feature_extraction.text import CountVectorizer

def create_name(token):
  name = []
  for child in token.children:
    if child.dep_ == "compound":
      name.append(child.text)
  name.append(token.text)
  return " ".join(name)

def calculate_average_vector(vectors):
  result = np.zeros(vectors.shape[1])
  for vector in vectors:
    result = np.add(result, vector)
  result = result / vectors.shape[0]
  print(result)
  return True

def remove_stop_words(sentence):
  doc = nlp(u'{}'.format(sentence))
  # results = [(token, token.lemma_, token.pos_, token.tag_) for token in doc if not token.is_stop]
  results = [str(token) for token in doc if not token.is_stop]
  results = (' ').join(results)
  return results

# def find_actors_index(doc):
#   for index, token in enumerate(doc):
#     if token.text == "with" or token.text == "starring":
#       doc = doc[index:]
#       strDoc = []
#       for token in doc:
#         strDoc.append(token.text)
#       doc = ' '.join(strDoc)
#       return doc
#     print("Test")

def test():
  # crew = ["Brad Pitt", "Ana Armas", "Ana armas", "John Film"]
  # crew_in_db = set()
  # crewPresent = True
  # for crew_member in crew:
  #   db_search = getCrewBySimilarName(crew_member.lower())
  #   if db_search:
  #     crew_in_db.add((db_search['CrewID'], db_search['Name']))
  # crew_in_db = list(crew_in_db)
  # if(len(crew_in_db)) > 3:
  #   crew_in_db = crew_in_db[:3]
  # print(list(crew_in_db))
  # questions = [
    # u'can you suggest a film similar to the Lord of the Rings and The Two Towers',
  #   u'can you suggest a film like Shrek',
  #   u'can you suggest a movie that is like Superman',
  #   u'give me a film similar to the Wizard Of Oz'
  # ]
  # doc = nlp(u'give me a film similar to The Wizard Of Oz')
  # for ent in doc.ents:
  #   print(ent, ent.label_)


  # doc = nlp( u'can you suggest a film similar to the Lord of the Rings and The Two Towers'.lower())
  # doc = nlp(u'The Hangover And Superman Which is a Comedy')
  doc = nlp(u"The Lion The Witch And The Wardrobe")

  displacy.serve(doc, style='dep')
  # rs = [token.text for token in doc if not token.is_stop]
  # rs = ' '.join(rs)
  # doc = nlp(u'{}'.format(rs))
  # doc = nlp(u'Shrek')
  # for ent in doc.ents:
  #   print(ent, ent.label_)
  # for token in doc:
    # if token.text == "to":
      # for anc in token.ancestors:
      #   if anc.text == "similar":
      #     for ancAnc in anc.ancestors:
      #       if ancAnc.text == "film":
      #         print("Yeah")
        # print(anc)
      # position = token.i
      # token_index_minus_one = doc[position - 1]
      # token_index_minus_two = doc[position - 2]
      # if token_index_minus_one.is_ancestor(token) and token_index_minus_one.text == "similar" and token_index_minus_two.is_ancestor(token_index_minus_one) and (token_index_minus_two.text == "film" or token_index_minus_two.text == "movie"):
      #   print("yeet")

  #   if token.text == "like":
  #     position = token.i
  #     previous_token = doc[position - 1]
  #     if previous_token.is_ancestor(token) and (previous_token == "film" or previous_token == "movie"):
  #       print("yote")



      # print(u"similar" in token.ancestors)
  # for ent in doc.ents:
  #   print(ent, ent.label_)
  # for q in questions:
  #   doc = nlp(q)
  #   for ent in doc.ents:
  #     print(ent, ent.label_)
  # displacy.serve(doc, style='dep')

  #"Can you suggest tom cruise" -> suggest (verb) -> cruise (noun) (compound)-> tom (noun)
  #"Can you suggest starring ben affleck" -> suggest(verb) -> affleck(propnoun) (compound) -> ben(X)
  #"Can you suggest starring Ben Affleck" -> suggest(verb) -> affleck(propnoun) (compound) -> ben(propnoun)
  # doc = nlp(u"can you suggest a film starring esme creed-miles and lupita nyong'o and ana de armas")
  # message = u"can you suggest a film starring Ben Affleck and Tom Cruise and Ana de Armas".lower()
  # crew = set()
  # flag = False
  # docLower = nlp(message)
  # while not flag:
  #   for token in docLower:
  #     if token.text == "with" or token.text == "starring":
  #       message2 = message[token.idx:]
  #       flag = True

  # if flag:
  #   docLower2 = nlp(message2.title())
  #   for child in docLower2[0].children:
  #     if child.pos_ == "NOUN" or child.pos_ == "PROPN":
  #         crew.add(create_name(child))
  #         for conjunct in child.conjuncts:
  #           crew.add(create_name(conjunct))
  # # docLower = find_actors_index(docLower)
  # # for token in docLower:
  #   # if token.text == "with" or token.text == "starring":
  #     # docLower[token.i:].title()
  #     # for child in token.children:
        

  # print(list(crew))
  
  # doc = nlp(u"can you suggest a film With Ben Affleck And Tom Cruise And Ana De Armas which is a comedy".lower())
  # displacy.serve(doc, style='dep')

  # # for token in doc:
  # #   if token.text == "with" or token.text == "starring":
  # #   for child in token.children:
  # #     print(child)
  # # # print(nlp(u'with')[0].is_stop)
  # # print("with" in nlp.Defaults.stop_words)
  # # nlp.Defaults.stop_words.remove('with')
  # # print("with" in nlp.Defaults.stop_words)
  # # print(nlp.vocab[u'is'].is_stop)
  # # print(nlp(u'with')[0] in nlp.Defaults.stop_words)
  # # doc2 = nlp(u"Can you suggest a film with tom cruise")
  # # print(remove_stop_words(doc))
  # print(remove_stop_words(doc2))

  # a(doc)
  # a(doc2)
  # for token in doc:
  #     print(token.text, token.dep_, token.head.text, token.head.pos_,
  #             [child for child in token.children])
  # displacy.serve(doc, style='dep')
  # displacy.serve(doc2, style='dep')
  # message = u'Can you suggest a film like the wizard of oz'
  # message = nlp(message)
  # # Get MESSAGE "MOVIE LIKE/FILM LIKE POSITION THEN GET THEIR CHILDREN"
  # for ent in message.ents:
  #   print(ent.text)
    # if ent.label_ == "WORK_OF_ART":
    #   print(ent.text)
  # data = [
  #   {"Name": "FirstFilm", "Metadata": "comedy action nm123"},
  #   {"Name": "SecondFilm", "Metadata": "action nm124 nm12"},
  #   {"Name": "ThirdFilm", "Metadata": "thriller action nm123"}
  #   ]
  # df = pd.DataFrame(data, columns=["Name", "Metadata"])
  # print(df.head())
  
  # cv = CountVectorizer(stop_words='english')
  # cv_matrix = cv.fit_transform(df['Metadata'])
  # vectors = cv_matrix.todense()
  # calculate_average_vector(vectors)
  
  
  return True


if __name__ == '__main__':
  test()


    # for token in docLower:
    # if token.text == "with" or token.text == "starring":
    #   for child in token.children:
    #     if child.pos_ == "NOUN" or child.pos_ == "PROPN":
    #       crew.add(create_name(child))
    #       for conjunct in child.conjuncts:
    #         crew.add(create_name(conjunct))