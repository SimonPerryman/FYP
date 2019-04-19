# Sentiment Analysis
import sys
import os
from time import time
sys.path.insert(0, os.environ['APPLICATION_PATH'])

import database as db

def check_for_users_with_suggested_films():
    """Checks for users who the bot has suggested films for. 
    Increases the ask counter once so that they do not ask the user constantly
    and sets their context to be about asking for a film review.
    @returns {List} users"""
    currentTime = ()
    users = db.getAllUsersWithSuggestedFilms()
    users_to_message = []
    for user in users:
         if (currentTime - user['SuggestedFilmTime']) < (86400 * user['Asked'] + 1):
             users_to_message.append(user)

    db.setAskedCounter([(user['UserID'], user['Asked']) for user in users])
    db.setAskFilmReview([
        (
            db.contexts['FilmReview'],
            db.stages['filmReview']['AskIfWatched'],
            user['Context'],
            user['Stage'],
            user['UserID']
        )
        for user in users])
    return users
    
def ask_for_film_review(bot, job):
    """Asks users if they have watched the suggested film"""
    users = check_for_users_with_suggested_films()
    if users:
        for user in users:
            db_query = db.getFilmByID(user['SuggestedFilm'])
            if db_query:
                requested_film = "".join([film['Title'] for film in db_query])    
                bot.send_message(chat_id=user['UserID'], "Hi {}, have you managed to watch {} yet?".format(user['FirstName'], requested_film))

def film_review_handler(bot, update, User):
    