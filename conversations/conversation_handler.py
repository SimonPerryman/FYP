from time import time
from .chitchat import moodMessage, greetingsMessage
from .registration import registrationHandler
from .film_suggestion import FilmSuggestionHandler
from .film_review import filmReviewHandler
from database import contexts
from botAssets import feeling, greetings
from nlp_techniques import lemmatize_sentence, check_for_expected_input
import database as db
import spacy
nlp = spacy.load('en_core_web_lg')

from database import getUser, getFavouriteGenres

def calculate_if_new_conversation(User, intent, currentTime):
    """Estimates if the message is the start is the start of a new conversation
    @param {Person} User
    @param {Int} intent - estimated intent of message
    @param {Int} currentTime
    @returns 1 if new conversation, else 0"""
    if (User.last_message < currentTime - 172800) or intent == 1:
        return 1
    return 0

def identify_intent(message):
    """Identify the intent of the given message
    @param {String} message
    @returns {Int} intent"""
    doc = nlp(message.lower())
    filmSuggestionSimilarity = nlp(u'can you suggest a film for me to watch').similarity(doc)
    howAreYouSimilarity = nlp(u"how are you feeling today").similarity(doc)
    intent = 0
    if message.lower() in greetings:
        intent = 1
    elif check_for_expected_input(lemmatize_sentence(message), feeling) or (howAreYouSimilarity > filmSuggestionSimilarity and howAreYouSimilarity > 0.70):
        intent = 2
    elif (filmSuggestionSimilarity > howAreYouSimilarity and filmSuggestionSimilarity > 0.70):
        intent = 3

    return intent

def conversation_handler(bot, update):
    """Handler function to call the correct function depending on the estimated intent
    of the message.
    @param {Bot} bot
    @param {update} update"""
    currentTime = int(time())
    message = update.message.text
    intent = identify_intent(message)
    userDetails = getUser(update.message.chat.id)
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
    db.setLastMessage(User.id, currentTime)
    NewConversation = calculate_if_new_conversation(User, intent, currentTime)
    db.insertMessage(User.id, message, currentTime, intent, User.context, User.stage, NewConversation)
    if User.context == contexts['InitialUserRegistration']:
        registrationHandler(bot, update, User)
    elif User.context == contexts['FilmReview']:
        filmReviewHandler(bot, update, User)
    elif intent == 1:
        greetingsMessage(bot, update)
    elif intent == 2:
        moodMessage(bot, update)
    elif User.context == contexts['FilmSuggestion'] or intent == 3:
        FilmSuggestionHandler(bot, update, User)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry I don't understand what you said. I currently can suggest films, review films and talk about my day!")
  