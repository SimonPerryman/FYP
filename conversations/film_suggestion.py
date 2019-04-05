import spacy
import re
from database import (getAllGenres, getAllAlternativeGenreNames, getCrewBySimilarName, 
                      getFilmBySimilarName, getFilmByProcessedName, insert_query_information,
                      get_query_info, setUserContextAndStage, contexts, stages, remove_query_info)
nlp = spacy.load('en_core_web_lg')

def preprocess_film_name(film_name):
  """Preprocess the film name and returns it
  @param {String} film_name
  @returns Preprocessed film name"""
  return re.sub(r"[^\s^\d^\w]", "", film_name).replace(" ", "")

def format_query_info(message_data):
  """Formats the data passed to the function
  @param message_data {List} - list of data to format
  @returns formatted string with all the data"""
  if len(message_data) == 3:
    message = " and ".join(message_data[:2])
    return message + ", and {}".format(message_data[2])
  return " and ".join(message_data)


def search_for_film_in_db(preprocessed_film_name):
  """Searches the databased for preprocessed film names, trying first the exact string,
  then using the SQL LIKE command, with the like operator %.
  @param preprocessed_film_name {String}
  @returns database result if there was a result, else an empty dictionary"""
  db_query = getFilmByProcessedName(preprocessed_film_name)
  if db_query:
    return db_query
  else:
    db_query = getFilmBySimilarName(preprocessed_film_name)
    if db_query:
      return db_query
  return {}

def search_for_film_start(message):
  """Searches the message for what is believed to be the start of the film title
  @param message {String}
  @returns index of the start of the film title and the substring of the message,
  starting at the index previously mentioned. Index of 0 and the message string is
  returned if the film title is not found."""
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
  """Iterates through the message, working backwards, creating n-grams (substrings) to
  search the database incase it matches a preprocessed film title. If there is only a 
  unigram left (one word substring), check if it is a noun or proper noun first.
  @param message {String}
  @returns Title of Film (not preprocessed version), empty dictionary if not found"""
  doc = nlp(u'{}'.format(message))
  first_word_is_useful = doc[0].pos_ == "NOUN" or doc[0].pos_ == "PROPN"
  for index in range(len(doc), 0, -1):
    if index > 1 or first_word_is_useful:
      preprocessed_film_name = preprocess_film_name(doc[:index.text])
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        return db_query['Title']
  return {}

def create_name(token):
  """Creates the name of the crew member found in the text.
  @param token {Token}
  @return {String} Name"""
  name = []
  for child in token.children:
    if child.dep_ == "compound":
      name.append(child.text)
  name.append(token.text)
  return " ".join(name)

def check_for_genres(message):
  """Searches the message for specific genres.
  @param {String} message
  @returns {List} genre names
  """
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
  """Searches for crew members in the message using NER and then checks
  for keywords which a crew member's name would be expected to be followed by.
  @param {String} message
  @returns {List} crew names"""
  crew = set()
  crew_present = False
  doc = nlp(u'{}'.format(message))
  docLower = nlp(u'{}'.format(message.lower()))
  # Use in built entity #TODO proper name
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      crew.add(ent.text)
  
  # Using Preprocessing and Dependency #TODO proper name
  
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
  """Searches the message for a film title using Named Entity Recognition (NER)
  and checks for film titles using the n-gram iteration method.
  @param {String} message
  returns {List} Film Titles
  """
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

def extract_film(UserID, message):
  film = check_for_film(message)
  if film:
    for film_name in film:
      preprocessed_film_name = preprocess_film_name(film_name)
      
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        film_in_db.add(db_query['FilmID'])
    film_in_db = list(film_in_db)

    if film_in_db:
      if len(film_in_db) > 3:
        film_in_db = film_in_db[:3]
      for film in film_in_db:
        insert_query_information(UserID, film, 1)
      return True
  return False

def extract_data(bot, message, User):
  """Calls the functions to search for the genre, film and crew information
  and inserts the relevant information into the database.
  @param {Obj} bot
  @param {String} message
  @param {Obj} User"""
  genres = check_for_genres(message)
  crew = check_for_crew(message)
  film = check_for_film(message)
  film_in_db = set()
  next_stage = 'AskFilm'

  # Noun chunks for <bad>/<funny> etc
  if genres:
    if len(genres) > 3:
      genres = genres[:2]

    for genre in genres:
      insert_query_information(User.id, genre, 2)

  if crew:
    crew_in_db = set()
    for crew_member in crew:
      db_query = getCrewBySimilarName(crew_member)
      if db_query:
        crew_in_db.add((db_query['CrewID'], db_query['Name']))
    crew_in_db = list(crew_in_db)
    if len(crew_in_db) > 3:
      crew_in_db = crew_in_db[:3]
    
    if crew_in_db:
      for crew in crew_in_db:
        insert_query_information(User.id, crew, 3)

  # insert film information
  if film:
    for film_name in film:
      preprocessed_film_name = preprocess_film_name(film_name)
      
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        film_in_db.add(db_query['FilmID'])
    film_in_db = list(film_in_db)

    if film_in_db:
      if len(film_in_db) > 3:
        film_in_db = film_in_db[:3]
      for film in film_in_db:
        insert_query_information(User.id, film, 1)
      next_stage = 'ConfirmFilm'
  #
  
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])
  if next_stage == 'AskFilm':
    bot.send_message(User.id, "Do you want the film I suggest to be similar to another film?")
  else:
    films = format_query_info(film_in_db)
    bot.send_message(User.id, "So you want a film similar to {}?".format(films))

def confirm_film_response(bot, message, User):
  """Stage 2 Response. Confirming the extracted film information was correct.
  @param {Obj} bot
  @param {String} message
  @param {Obj} User"""
  yes = nlp(u"yes")
  no = nlp(u"no")
  skip = False
  next_question_message = "Error lol"
  next_stage = 'ConfirmFilm'
  doc = nlp(u"{}".format(message))
  for token in doc:
    if token.lower_ == "skip":
      skip = True
  # USE LEMMAS TO REPLACE YES/NO
  if yes.similarity(doc) > 0.8 or skip:
    #TODO CHECK FOR ADDING OF FILMS/REMOVING OF FILMS
    genres_query_info = get_query_info(User.id, 2)
    if genres_query_info:
      genres = format_query_info(genres_query_info)
      if skip:
        next_question_message = "ite skipping this section. I will suggest a film with the following genres {}".format(genres)
      else:
        next_question_message = "You said yes so we are moving on... I will suggest the following genres {}".format(genres)
      next_stage = 'ConfirmGenre'
    else:
      if skip:
        next_question_message = "ite skipping this section. You want any genres"
      else:
        next_question_message = "You said yes so we are moving on... You want any genres?"
      next_stage = 'AskGenre'
  elif no.similarity(doc) > 0.8:
    next_stage = 'AskFilm'
    next_question_message = "Ok, so do you want the film I suggest to be similar to another film?"
    remove_query_info(User.ID, 1)
  
  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])
    
def ask_film_response(bot, message, User):
  films = set()
  films_in_db = set()
  skip = False
  next_stage = 'AskFilm'
  next_question_message = "Sorry didn't quite catch that - did you want a film to be like another"
  doc = nlp(u'{}'.format(message))
  for token in doc:
    if token.lower_ == "skip":
      skip = True
  if skip or skip == "No": #TODO CHECK HOW TO SEE YES/NO
    genres_query_info = get_query_info(User.id, 2)
    if genres_query_info:
      genres = format_query_info(genres_query_info)
      next_question_message = "Ok. So you want a film that is a {} too".format(genres)
      next_stage = 'ConfirmGenre'
    else:
      next_question_message = "Ok, do you want the film to be for any specific genre?"
      next_stage = 'AskGenre'
  else:
    for ent in doc.ents:
      if ent.label_ == "WORK OF ART" or ent.label_ == "PERSON" or ent.label_ == "PRODUCT" or ent.label_ == "ORG":
        films.add(ent.text)
    if films:
      for film in films:
        found_film = search_for_film_in_db(preprocess_film_name(film))
        films_in_db.add(found_film)
    mined_film_titles = iterate_through_ngrams(message)
    for film_title in mined_film_titles:
      films_in_db.add(film_title)
    films_in_db = list(films_in_db)
    if films_in_db:
      if len(films_in_db) > 3:
        films_in_db = films_in_db[:2]
      for film in films_in_db:
        insert_query_information(User.id, film, 1)
      films = format_query_info(films_in_db)
      next_question_message = "So you want a film similar to {}?".format(films)
      next_stage = 'ConfirmFilm'

  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])

def confirm_genre_response(bot, message, User):
  print(True)

def FilmSuggestionHandler(bot, update, User):
  message = update.message.text
  if User.stage == 1:
    extract_data(bot, message, User)
  if User.stage == 2:
    confirm_film_response(bot, message, User)
  if User.stage == 3:
    ask_film_response(bot, message, User)
  if User.stage == 4:
    confirm_genre_response(bot, message, User)
  print("Film Suggestion Handler")