import spacy
import re
from database import getAllGenres, getAllAlternativeGenreNames, getCrewBySimilarName, getFilmBySimilarName, getFilmByProcessedName
nlp = spacy.load('en_core_web_lg')

def search_for_film_in_db(preprocessed_film_name):
  db_query = getFilmByProcessedName(preprocessed_film_name)
  if db_query:
    return db_query
  else:
    db_query = getFilmBySimilarName(preprocessed_film_name)
    if db_query:
      return db_query
  return {}

def search_for_film_start(message):
  accepted_film_synonyms = ["movie", "film", "something"]
  doc = nlp(message)
  genres = [genre['Name'] for genre in getAllGenres()]
  index = 0
  for token in doc:
    if token.text == "to":
      for anc in token.ancestors:
        if anc.text == "similar":
          for rec_anc in anc.ancestors:
            if rec_anc.text in accepted_film_synonyms or rec_anc.text in genres:
              index = token.idx + len(token) + 1
              return index, message[index:]

    if token.text == "like":
      position = token.i
      previous_token = doc[position - 1]
      if previous_token.is_ancestor(token) and (previous_token.text in accepted_film_synonyms or previous_token.text in genres):
        index = token.idx + len(token) + 1
        return index, message[index:]

  return 0, message

def iterate_through_ngrams(message):
  doc = nlp(u'{}'.format(message))
  first_word_is_useful = doc[0].pos_ == "NOUN" or doc[0].pos_ == "PROPN"
  for index in range(len(doc), 0, -1):
    if index > 1 or first_word_is_useful:
      preprocessed_film_name = re.sub(r"[^\s^\d^\w]", "", doc[:index].text).replace(" ", "")
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        return db_query['Title']
  return {}

def create_name(token):
  name = []
  for child in token.children:
    if child.dep_ == "compound":
      name.append(child.text)
  name.append(token.text)
  return " ".join(name)

def check_for_genres(message):
  docLower = nlp(u'{}'.format(message.lower()))
  genres = set()
  genresInfo = getAllGenres()
  for genre in genresInfo:
    for token in docLower:
      if token.text == genre['Name']:
        genres.add(genre['Name'])

  alternativeGenreNamesInfo = getAllAlternativeGenreNames()
  for alternativeGenreInfo in alternativeGenreNamesInfo:
    for token in docLower:
      if token.text == alternativeGenreInfo['AlternativeName']:
        genres.add(alternativeGenreInfo['Name'])

  return list(genres)

def check_for_crew(message):
  crew = set()
  doc = nlp(u'{}'.format(message))
  docLower = nlp(u'{}'.format(message.lower()))
  # Use in built entity #TODO proper name
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      crew.add(ent.text)
  
  # Using Preprocessing and Dependency #TODO proper name
  crew_present = False

  for token in docLower:
    if token.text == "with" or token.text == "starring":
      message = message[token.idx:].title()
      crew_present = True

  if crew_present:
    doc = nlp(message)
    for child in doc[0].children:
      if child.pos_ == "NOUN" or child.pos_ == "PROPN":
          crew.add(create_name(child))
          for conjunct in child.conjuncts:
            crew.add(create_name(conjunct))

  return list(crew)

def check_for_film(message):
  film = set()
  doc = nlp(u'{}'.format(message))
  for ent in doc.ents:
    # Person as that includes fictional people, such as superman.
    if ent.label_ == "WORK OF ART" or ent.label_ == "PERSON" or ent.label_ == "PRODUCT" or ent.label_ == "ORG":
      film.add(ent.text)

  film_present, message = search_for_film_start(message)
  if film_present != 0:
    db_query = iterate_through_ngrams(message)
    if db_query:
      film.add(db_query)

  return list(film)

def FilmSuggestionHandler(bot, update, User):
  genresPresent = False
  crewPresent = False
  filmPresent = False
  crew_in_db = set()
  film_in_db = set()

  message = update.message.text
  
  genres = check_for_genres(message)
  crew = check_for_crew(message)
  film = check_for_film(message)

  # Noun chunks for <bad>/<funny> etc
  if genres:
    genresPresent = True
    if len(genres) > 3:
      genres = genres[:2]

  if crew:
    for crew_member in crew:
      db_query = getCrewBySimilarName(crew_member)
      if db_query:
        crew_in_db.add((db_query['CrewID'], db_query['Name']))
    crew_in_db = list(crew_in_db)
    if len(crew_in_db) > 3:
      crew_in_db = crew_in_db[:3]
    
    if crew_in_db:
      crewPresent = True

  if film:
    for film_name in film:
      preprocessed_film_name = re.sub(r"[^\s^\d^\w]", "", film_name).replace(" ", "")
      
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        film_in_db.add((db_query['FilmID'], db_query['Title']))
    film_in_db = list(film_in_db)
    if len(film_in_db) > 3:
      film_in_db = film_in_db[:3]
    
    if film_in_db:
      filmPresent = True

  # Can get rid of XPresent
  # filmsTable = getFilmsTable()
  # filmsTable[]

  #Convert Film_in_DB and CREW_IN_DB to LIST whether they are found or not
  print(genres, type(genres))
  print(film_in_db, type(film_in_db))
  print(crew_in_db, type(crew_in_db))

  print(True)