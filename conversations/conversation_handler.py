from .chitchat import *
from .registration import registrationHandler
from .film_suggestion import FilmSuggestionHandler
from context import contexts
import spacy
nlp = spacy.load('en_core_web_lg')

from database import getUser, getFavouriteGenres

def identify_intent(message):
    intent = 0

    # Film Intent = 1 - Maybe gotta have here if they in filmSuggestion context - any stage bar 0/1?
    filmSuggestionExample = nlp(u'can you suggest a film for me to watch')
    if filmSuggestionExample.similarity(nlp(u'{}'.format(message.lower()))) > 0.70:
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
            self.suggested_film_index = userDetails.get('SuggestedFilmIndex', 0)
            favouriteGenres =  getFavouriteGenres(userDetails['UserID'])
            for genre in favouriteGenres:
                if genre.get('Order', 0) == 1:
                    self.favouriteGenre = genre.get('Name', 0)
                elif genre.get('Order', 0) == 2:
                    self.secondFavouriteGenre = genre.get('Name', 0)
                elif genre.get('Order', 0) == 3:
                    self.thirdFavouriteGenre = genre.get('Name', 0)
                    
    User = Person()
    if User.context == contexts['InitialUserRegistration']:
        registrationHandler(bot, update, User)
    elif User.context == contexts['FilmSuggestion'] or intent == 1:
        FilmSuggestionHandler(bot, update, User)
  

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
