import spacy
from database import getAllGenres, getAllAlternativeGenreNames
nlp = spacy.load('en_core_web_lg')

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

def check_for_crew(doc):
  crew = set()
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      crew.add(ent.text)
  return list(crew)

def check_for_film(doc):
  film = set()
  # for WORK_OF_ART

def FilmSuggestionHandler(bot, update, User):
  genresPresent = False
  crewPresent = False
  filmPresent = False

  message = update.message.text
  doc = nlp(u'{}'.format(message))
  genres = check_for_genres(message)
  crew = check_for_crew(doc)
  if genres:
    print("There were genres")
    genresPresent = True
    if len(genres) > 3:
      genres = genres[:2]
  if crew:
    print("There were crew")
    crewPresent = True
    if len(crew) > 3:
      crew = crew[:3]
  # if 
  # Generate Film (genres if genresPresent else None, )
  print(True)