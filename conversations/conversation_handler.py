from time import time
from .chitchat import *
from .registration import registrationHandler
from .film_suggestion import FilmSuggestionHandler
from .film_review import filmReviewHandler
from database import contexts
from botAssets import feeling
from nlp_techniques import lemmatize_sentence, check_for_expected_input
import database as db
import spacy
nlp = spacy.load('en_core_web_lg')

from database import getUser, getFavouriteGenres

def identify_intent(message):
    filmSuggestionExample = nlp(u'can you suggest a film for me to watch')
    howAreYouExample = nlp(u"how are you feeling today")
    doc = nlp(message.lower())
    intent = 0

    if howAreYouExample.similarity(doc) > 0.70 or check_for_expected_input(lemmatize_sentence(message), feeling):
        intent = 2
    elif filmSuggestionExample.similarity(doc) > 0.70:
        intent = 1

    return intent

def conversation_handler(bot, update):
    userDetails = getUser(update.message.chat.id)
    intent = identify_intent(update.message.text)
    class Person:
        def __init__(self):
            self.id = userDetails['UserID']
            self.first_name = userDetails['FirstName']
            self.last_name = userDetails.get('LastName', '')
            self.age = userDetails.get('Age', 0)
            self.context = userDetails.get('Context', 0)
            self.stage = userDetails.get('Stage', 0)
            self.last_message = userDetails.get('LastMessage', 0)
            self.suggested_film = userDetails.get('SuggestedFilm', 0)
            self.suggested_film_index = userDetails.get('SuggestedFilmIndex', 0)
            self.previous_context = userDetails.get('PreviousContext', 0)
            self.previous_stage = userDetails.get('PreviousStage', 0)
            favouriteGenres =  getFavouriteGenres(userDetails['UserID'])
            for genre in favouriteGenres:
                if genre.get('Order', 0) == 1:
                    self.favouriteGenre = genre.get('Name', 0)
                elif genre.get('Order', 0) == 2:
                    self.secondFavouriteGenre = genre.get('Name', 0)
                elif genre.get('Order', 0) == 3:
                    self.thirdFavouriteGenre = genre.get('Name', 0)
                    
    User = Person()
    db.setLastMessage(User.id, int(time()))
    if User.context == contexts['InitialUserRegistration']:
        registrationHandler(bot, update, User)
    elif User.context == contexts['FilmReview']:
        filmReviewHandler(bot, update, User)
    elif User.context == contexts['FilmSuggestion'] or intent == 1:
        FilmSuggestionHandler(bot, update, User)
        
  

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
