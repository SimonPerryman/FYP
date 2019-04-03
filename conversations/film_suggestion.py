import spacy
from database import getAllGenres, getAllAlternativeGenreNames, getCrewBySimilarName, getFilmBySimilarName
nlp = spacy.load('en_core_web_lg')

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
      db_search = getCrewBySimilarName(crew_member)
      if db_search:
        crew_in_db.add((db_search['CrewID'], db_search['Name']))
    crew_in_db = list(crew_in_db)
    if len(crew_in_db) > 3:
      crew_in_db = crew_in_db[:3]
    
    if crew_in_db:
      crewPresent = True

  if film:
    for film_name in film:
      db_search = getFilmBySimilarName(film_name)
      if db_search:
        film_in_db.add((db_search['FilmID'], db_search['Title']))
    film_in_db = list(film_in_db)
    if len(film_in_db) > 3:
      film_in_db = film_in_db[:3]
    
    if film_in_db:
      filmPresent = True

  # filmsTable = getFilmsTable()
  # filmsTable[]

  #Convert Film_in_DB and CREW_IN_DB to LIST whether they are found or not
  print(genres, type(genres))
  print(film_in_db, type(film_in_db))
  print(crew_in_db, type(crew_in_db))

  print(True)