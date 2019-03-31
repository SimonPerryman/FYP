from .chitchat import *
from .films import *
from .registration import registrationHandler
from context import contexts

from database import getUser, getFavouriteGenres

def conversation_handler(bot, update):
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

            favouriteGenres =  getFavouriteGenres(userDetails['UserID'])
            if len(favouriteGenres) > 0:
                self.favouriteGenre = favouriteGenres[0]
                if len(favouriteGenres) > 1:
                    self.secondFavouriteGenre = favouriteGenres[1]
                    if len(favouriteGenres) > 2:
                        self.thirdFavouriteGenre = favouriteGenres[2]

    User = Person()
    if User.context == contexts['InitialUserRegistration']:
        registrationHandler(bot, update, User)
  

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
