import spacy
import re
import database as db
import pandas as pd
from database import setUserContextAndStage, contexts, stages
from recommendation_system import hybrid_recommender
from nlp_techniques import lemmatize_sentence, check_for_expected_input
from misc import get_imdb_film_details
from botAssets import positives, negatives, negative_film_responses, skip, cancel
nlp = spacy.load('en_core_web_sm')

def generate_film(bot, User, index):
  """Generates a suggested film for the user using the query information
  and the hybrid recommender. If errors, send an error message and resets
  user stage/context to chitchat.
  @param {Bot} bot
  @param {Person} User
  @param {Int} index"""
  suggested_films = hybrid_recommender(User)
  try:
    suggested_film = suggested_films.iloc[index]
    suggested_film_poster_url, suggested_film_plot = get_imdb_film_details(suggested_film['FilmID'])
    db.updateSuggestedFilm(User.id, suggested_film['FilmID'])
    next_question_message = "I have found this film, which I think you will like: {}".format(suggested_film['Title'])
    bot.send_message(User.id, next_question_message)
    if suggested_film_poster_url:
      bot.send_photo(User.id, photo=suggested_film_poster_url)
    if suggested_film_plot:
      bot.send_message(User.id, "Here is the plot of the film:\n{}".format(suggested_film_plot))
    setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion']['SuggestedFilm'])
  except Exception as e:
    bot.send_message(User.id, "I am currently struggling to suggest a similar film for you, please ask me again later.")
    setUserContextAndStage(User.id, contexts['ChitChat'], stages['ChitChat'])
    print("Error suggesting a film", str(e))

def preprocess_text(film_name):
  """Preprocess the film name and returns it
  @param {String} film_name
  @returns Preprocessed film name"""
  return re.sub(r"[^\s^\d^\w]", "", film_name.lower()).replace(" ", "")

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
  db_query = db.getFilmByProcessedName(preprocessed_film_name)
  if db_query:
    return db_query
  else:
    db_query = db.getFilmBySimilarName(preprocessed_film_name)
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
  genres = [genre['Name'] for genre in db.getAllGenres()]
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
      preprocessed_film_name = preprocess_text(doc[:index].text)
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        return (db_query['FilmID'], db_query['Title'])
  return {}

def create_name(token):
  """Creates the name of the crew member found in the text.
  @param token {Token}
  @returns {String} Name"""
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
  genresInfo = db.getAllGenres()
  for genre in genresInfo:
    for token in docLower:
      if token.text == genre['Name']:
        genres.add(genre['Name'])

  alternativeGenreNamesInfo = db.getAllAlternativeGenreNames()
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
  @returns {List} Film Titles
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
      film.add(db_query[1])

  return list(film)

def extract_film(UserID, message):
  """Function to call other subfunctions to extract film  data,
  insert into the database and then return film titles.
  @param {Int} UserID
  @param {String} message
  @return {List} Film Titles, empty if none found"""
  film = check_for_film(message)
  film_in_db = set()
  if film:
    for film_info in film:
      preprocessed_film_name = preprocess_text(film_info)
      
      db_query = search_for_film_in_db(preprocessed_film_name)
      if db_query:
        film_in_db.add((db_query['FilmID'], db_query['Title']))
    film_in_db = list(film_in_db)

    if film_in_db:
      if len(film_in_db) > 3:
        film_in_db = film_in_db[:3]
      for film in film_in_db:
        db.insertQueryInformation(UserID, film[0], 1)
      return [film[1] for film in film_in_db]
  return []

def extract_genres(UserID, message):
  """Function to call other subfunctions to extract genres,
  then insert the data into the db.
  @param {Int} UserID
  @param {String} message
  @returns {List} Genre names, empty if none found"""
  genres = check_for_genres(message)
  if genres:
    if len(genres) > 3:
      genres = genres[:2]
    
    for genre in genres:
      db.insertQueryInformation(UserID, genre, 2)
    
    return genres
  return []
  
def extract_crew(UserID, message):
  """Function to call other subfunctions to extract crew members,
  then insert the data into the database.
  @param {Int} UserID
  @param {String} message
  @returns {List} Crew Member Names, Empty if none found"""
  crew = check_for_crew(message)
  if crew:
    crew_in_db = set()
    for crew_member in crew:
      db_query = db.getCrewBySimilarName(crew_member)
      if db_query:
        crew_in_db.add((db_query['CrewID'], db_query['Name']))
    crew_in_db = list(crew_in_db)
    if len(crew_in_db) > 3:
      crew_in_db = crew_in_db[:3]

    if crew_in_db:
      for crew in crew_in_db:
        db.insertQueryInformation(UserID, crew[0], 3)
      return [crew[1] for crew in crew_in_db]
  return []
  

def extract_data(bot, message, User):
  """Stage 1 Response. Calls the functions to search for the genre, film and
  crew information and inserts the relevant information into the database.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  #TODO Noun chunks for <bad>/<funny> etc
  db.removeQueryInfo(User.id)
  next_stage = 'AskFilm'
  extract_genres(User.id, message)
  extract_crew(User.id, message)
  films = extract_film(User.id, message)
  if films:
    next_stage = 'ConfirmFilm'
  
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])
  if next_stage == 'AskFilm':
    bot.send_message(User.id, "Do you want the film I suggest to be similar to another film?")
  else:
    filmTitles = format_query_info([film for film in films])
    bot.send_message(User.id, "So you want a film similar to {}?".format(filmTitles))

def confirm_film_response(bot, message, User):
  """Stage 2 Response. Confirming the extracted film information was correct.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  skipFlag = False
  db_query = db.getQueryInfo(User.id, 1)
  film_names = set()
  if db_query:
    for result in db_query:
      FilmName = db.getFilmByID(result['Information'])
      if FilmName:
        film_names.add(FilmName['Title'])
  next_question_message = "Sorry I'm not sure I understand."
  if film_names:
    film_names = format_query_info(list(film_names))
    next_question_message = next_question_message + " Did you want a film similar to {}".format(film_names)
  next_stage = 'ConfirmFilm'
  if check_for_expected_input(message, skip):
    skipFlag = True
  if check_for_expected_input(message, positives) or skipFlag:
    #TODO CHECK FOR ADDING OF FILMS/REMOVING OF FILMS
    genres_query_info = db.getQueryInfo(User.id, 2)
    if genres_query_info:
      genres = format_query_info([genre['Information'] for genre in genres_query_info])
      if skipFlag:
        next_question_message = "Ok let's skip choosing a similar film. I just want to confirm that you did want a film that was a {}".format(genres)
      else:
        next_question_message = "Alright that sounds good! I just want to confirm that you did want a film that was a {}".format(genres)
      next_stage = 'ConfirmGenre'
    else:
      if skipFlag:
        next_question_message = "Ok let's skip choosing a similar film. Did you want the film to have any specific genres?"
      else:
        next_question_message = "Alright that sounds good! Did you want the film to have any specific genres?"
      next_stage = 'AskGenre'
  elif check_for_expected_input(message, negatives):
    next_stage = 'AskFilm'
    next_question_message = "Ok, so do you want the film I suggest to be similar to another film?"
    db.removeQueryInfo(User.id, 1)

  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])
    
def ask_film_response(bot, message, User):
  """Stage 3 Response. Asking if the user wants the suggested film to be similar to
  another film.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  skipFlag = False
  next_stage = 'AskFilm'
  next_question_message = "Sorry I don't understand. Do you want the film to be similar to another film you've seen?"
  if check_for_expected_input(message, skip):
      skipFlag = True
  if skipFlag or check_for_expected_input(message, negatives):
    genres_query_info = db.getQueryInfo(User.id, 2)
    if genres_query_info:
      genres = format_query_info([genre['Information'] for genre in genres_query_info])
      next_question_message = "Ok. So you want a film that is a {}?".format(genres)
      next_stage = 'ConfirmGenre'
    else:
      next_question_message = "Ok, Did you want the film to have any specific genres?"
      next_stage = 'AskGenre'
  elif check_for_expected_input(message, positives):
    next_question_message = "Ok, what film do you want it to be similar to?"
  else:
    films = extract_film(User.id, message)
    #In case the user just sends the film title and nothing else
    preprocessed_message = preprocess_text(message)
    db_query = search_for_film_in_db(preprocessed_message)
    if db_query:
      film = (db_query['FilmID'], db_query['Title'])
      if film not in films:
        films.append(film)
        db.insertQueryInformation(User.id, film[0], 1)
    if films:
      filmTitles = format_query_info([film[1] for film in films])
      next_question_message = "So you want a film similar to {}?".format(filmTitles)
      next_stage = 'ConfirmFilm'

  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])

def confirm_genre_response(bot, message, User):
  """Stage 4 Response. Confirming the extracted genre information was correct.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  db_query = db.getQueryInfo(User.id, 2)
  genre = ''
  if db_query:
    genre = [query['Information'] for query in db_query]
  next_question_message = "Sorry I'm not sure I understand."
  if genre:
    next_question_message = next_question_message + " Did you want the film to be a {}".format(format_query_info(genre))
  next_stage = 'ConfirmGenre'
  skipFlag = False
  if check_for_expected_input(message, skip):
      skipFlag = True
  if skipFlag or check_for_expected_input(message, positives):
    crew_query_info = db.getQueryInfo(User.id, 3)
    if crew_query_info:
      crewIDs = [crew['Information'] for crew in crew_query_info]
      crew_names = []
      for crewID in crewIDs:
        crew_names.append(db.getCrewByID(crewID)['Name'])
      crew = format_query_info(crew_names)
      if skipFlag:
        next_question_message = "Ok, let's skip choosing a genre. From what you said earlier, you wanted {} to have been involved with the film?".format(crew)
      else:
        next_question_message = "Right, I'll note that down. From what you said earlier, you wanted {} to have been involved with the film?".format(crew)
      next_stage = 'ConfirmCrew'
    else:
      if skipFlag:
        next_question_message = "Ok let's skip choosing a genre. Are there any people you want to have been involved with the film?"
      else:
        next_question_message = "Right, I'll note that down. Are there any people you want to have been involved with the film?"
      next_stage = "AskCrew"
  elif check_for_expected_input(message, negatives):
    next_stage = 'AskGenre'
    next_question_message = "Ok, so are there any genres that you want the film to be of?"
    db.removeQueryInfo(User.id, 2)

  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])

def ask_genre_response(bot, message, User):
  """Stage 5 Response. Asking the user if they want the suggested film to be of a certain genre.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  skipFlag = False
  next_stage = 'AskGenre'
  next_question_message = "Sorry I'm not sure what you meant, were there any genres you had in mind for the film I will suggest?"
  if check_for_expected_input(message, skip):
      skipFlag = True
  if skipFlag or check_for_expected_input(message, negatives):
    crew_query_info = db.getQueryInfo(User.id, 3)
    if crew_query_info:
      crewIDs = [crew['Information'] for crew in crew_query_info]
      crew_names = []
      for crewID in crewIDs:
        crew_names.append(db.getCrewByID(crewID)['Name'])
      crew = format_query_info(crew_names)
      next_question_message = "ok so you want a film where {} was involved?".format(crew)
      next_stage = 'ConfirmCrew'
    else:
      next_question_message = "Ok so do you want a film with specific actors, directors or writers?"
      next_stage = 'AskCrew'
  elif check_for_expected_input(message, positives):
    next_question_message = "Ok, what genres did you have in mind?"
  else:
    genres = extract_genres(User.id, message)
    if genres:
      genres = format_query_info(genres)
      next_question_message = "So you want a film which is a {}?".format(genres)
      next_stage = 'ConfirmGenre'
  
  bot.send_message(User.id, next_question_message)
  setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])

def confirm_crew_response(bot, message, User):
  """Stage 6 Response. Confirming the extracted crew information was correct.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  skipFlag = False
  if check_for_expected_input(message, skip):
      skipFlag = True
  if skipFlag or check_for_expected_input(message, positives):
    generate_film(bot, User, 0)
    db.updateSuggestedFilmIndex(User.id, 0)
  elif check_for_expected_input(message, negatives):
    next_question_message = "Ok so did you want any specific people to have been involved with the film?"
    bot.send_message(User.id, next_question_message)
    setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion']['AskCrew'])
    db.removeQueryInfo(User.id, 3)
  else:
    db_query = db.getQueryInfo(User.id, 3)
    crew_names = []
    if db_query:
      for result in db_query:
        crew_names.append(db.getCrewByID(result['Information'])['Name'])
      crew_names = format_query_info(crew_names)
    next_question_message = "Sorry I don't understand."
    if crew_names:
      next_question_message = next_question_message + " Did you want a film with {}?".format(crew_names)
    bot.send_message(User.id, next_question_message)

def ask_crew_response(bot, message, User):
  """Stage 7 Response. Asking the user if they want the suggested film to include certain
  actors, actresses, directors or writers.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  generatedFilm = False
  skipFlag = False
  next_stage = 'AskCrew'
  next_question_message = "Sorry I'm not sure I understood correctly. Did you want any specific people to have been involved with the film?"
  if check_for_expected_input(message, skip):
      skipFlag = True
  if skipFlag or check_for_expected_input(message, negatives):
    generate_film(bot, User, 0)
    db.updateSuggestedFilmIndex(User.id, 0)
    generatedFilm = True
  elif check_for_expected_input(message, positives):
    next_question_message = "Ok, what are the names of these crew members?"
  else:
    crew = extract_crew(User.id, message)
    preprocessed_message = preprocess_text(message)
    db_query = db.getCrewByProcessedName(preprocessed_message)
    if db_query:
      crewInfo = (db_query['CrewID'], db_query['Name'])
      if crewInfo[1] not in crew:
        crew.append(crewInfo[1])
        db.insertQueryInformation(User.id, crew[0], 1)
    if crew:
      crew_names = format_query_info(crew)
      next_question_message = "So you want {} to have worked on the film?".format(crew_names)
      next_stage = 'ConfirmCrew'
  if not generatedFilm:
    bot.send_message(User.id, next_question_message)
    setUserContextAndStage(User.id, contexts['FilmSuggestion'], stages['filmSuggestion'][next_stage])

def confirm_suggested_film_response(bot, message, User):
  """Stage 8 Response. Checking the user's outcome of the suggested film
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  negative_film_responses.extend(negatives)
  if check_for_expected_input(message, positives):
    db.updateSuggestedFilmStatus(User.id, 1)
    db.updateSuggestedFilmIndex(User.id, 0)
    db.removeQueryInfo(User.id)
    bot.send_message(User.id, "Ok, have fun watching the film! Let me know what you thought of it!")
    setUserContextAndStage(User.id, contexts['ChitChat'], stages['ChitChat'])
  elif check_for_expected_input(message, negative_film_responses):
    bot.send_message(User.id, "Ok I am finding a new film that I think you will like.")
    new_index = User.suggested_film_index + 1
    generate_film(bot, User, new_index)
    db.updateSuggestedFilmIndex(User.id, new_index)
  else:
    bot.send_message(User.id, "Sorry I don't understand, is this film fine?")

def cancel_film_suggestion(bot, User):
  """Gets the user out of the film suggestion conversation
  @param {Bot} bot
  @param {Person} User"""
  db.updateSuggestedFilmStatus(User.id, 1)
  db.updateSuggestedFilmIndex(User.id, 0)
  db.removeQueryInfo(User.id)
  setUserContextAndStage(User.id, contexts['ChitChat'], stages['ChitChat'])
  bot.send_message(User.id, "Ok, that's fine. Just let me know if you do want me to suggest a film for you later.")

def FilmSuggestionHandler(bot, update, User):
  """Handler function to call the relevant function depending on
  what stage the user is on in the film suggestion journey.
  @param {Bot} bot
  @param {String} message
  @param {Person} User"""
  message = update.message.text
  if check_for_expected_input(message, cancel):
    cancel_film_suggestion(bot, User)
  elif User.stage == 1:
    extract_data(bot, message, User)
  elif User.stage == 2:
    confirm_film_response(bot, message, User)
  elif User.stage == 3:
    ask_film_response(bot, message, User)
  elif User.stage == 4:
    confirm_genre_response(bot, message, User)
  elif User.stage == 5:
    ask_genre_response(bot, message, User)
  elif User.stage == 6:
    confirm_crew_response(bot, message, User)
  elif User.stage == 7:
    ask_crew_response(bot, message, User)
  elif User.stage == 8:
    confirm_suggested_film_response(bot, message, User)
