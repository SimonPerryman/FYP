import sys
import os
from time import time
sys.path.insert(0, os.environ['APPLICATION_PATH'])
import database as db
from database import setUserContextAndStage, contexts, stages
from botAssets import positives, negatives, skip
from nlp_techniques import check_for_expected_input, perform_sentiment_analysis

def check_for_users_with_suggested_films():
    """Checks for users who the bot has suggested films for. 
    Increases the ask counter once so that they do not ask the user constantly
    and sets their context to be about asking for a film review.
    @returns {List} users"""
    currentTime = time()
    users = db.getAllUsersWithSuggestedFilms()
    users_to_message = []
    for user in users:
        timeFrame = currentTime - user['SuggestedFilmTime']
        threshold = 86400 * (user['Asked'] + 1)
        if timeFrame > threshold and user['LastMessage'] > (threshold - 86400):
            users_to_message.append(user)

    db.setAskedCounter([(user['Asked'] + 1, user['UserID']) for user in users_to_message])
    db.setAskFilmReview([
        (
            db.contexts['FilmReview'],
            db.stages['filmReview']['AskIfWatched'],
            user['Context'],
            user['Stage'],
            user['UserID']
        )
        for user in users_to_message])
        
    return users_to_message
    
def ask_for_film_review(bot, job):
    """Asks users if they have watched the suggested film
    @param {Bot}
    @param {job}"""
    users = check_for_users_with_suggested_films()
    if users:
        for user in users:
            db_query = db.getFilmByID(user['SuggestedFilm'])
            if db_query and type(db_query) is dict:
                bot.send_message(user['UserID'], "Hi {}, have you managed to watch {} yet?".format(user['FirstName'], db_query['Title']))

def AskIfWatchedResponse(bot, message, User):
    """Stage 1 Response. Asks the user if they will review the film.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    next_stage = 'AskIfWatchedResponse'
    next_message = ""
    next_context = "FilmReview"
    if check_for_expected_input(message, positives):
        next_message = "Excellent, would you like to review it for me?"
        next_stage = "AskReview"
    elif check_for_expected_input(message, negatives):
        next_message = "Ok, I hope you will watch it soon!"
        next_context = User.previous_context
        next_stage = User.previous_stage
    else:
        filmTitle = db.getFilmByID(User.suggested_film)['Title']
        next_message = "Sorry I didn't understand, have you seen {} yet?".format(filmTitle)
    bot.send_message(User.id, next_message)
    setUserContextAndStage(User.id, contexts[next_context], stages[next_context[0].lower() + next_context[1:]][next_stage])

def AskReviewResponse(bot, message, User):
    """Stage 2 Response. Asks the user for their review/asks if they will reconsider and give a review.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    next_stage = "AskReviewResponse"
    next_message = "Sorry I'm not sure I understand what you said."
    if check_for_expected_input(message, positives):
        next_message = "Ok, what is your review?"
        next_stage = "GiveReview"
    elif check_for_expected_input(message, negatives):
        next_message = "Are you sure? By reviewing films I can understand what you like more and suggest more accurate films!"
        next_stage = "ConfirmNoReview"
    
    bot.send_message(User.id, next_message)
    setUserContextAndStage(User.id, contexts['FilmReview'], stages['filmReview'][next_stage])

def GiveReviewResponse(bot, message, User):
    """Stage 3 Response. Analyse the review, stores it and asks the user to score the film from 1-5.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    next_stage = 'ScoreFilm'
    sentiment = perform_sentiment_analysis(message)
    db.insertReview(User.id, User.suggested_film, message, 1 if sentiment[0] == "pos" else 0, sentiment[1])
    bot.send_message(User.id, "Thanks for leaving your review! I have noted it down.")
    bot.send_message(User.id, "Could you also score the film out of 5? 1 being poor and 5 being excellent.")
    setUserContextAndStage(User.id, contexts['FilmReview'], stages['filmReview'][next_stage])

def ConfirmNoReviewResponse(bot, message, User):
    """Stage 4 Response. Ends the conversation and sets the stage/context back to previous values or,
    if the user changes their mind, takles asks them for their review.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    next_stage = stages['filmReview']["ConfirmNoReview"]
    next_message = "Sorry, I don't understand. Do you want to reconsider and give a review?"
    next_context = contexts['FilmReview']
    if check_for_expected_input(message, positives):
        db.removeSuggestedFilm(User.id)
        next_stage = User.previous_stage
        next_context = User.previous_context
        next_message = "Ok, no problem!"
    elif check_for_expected_input(message, negatives):
        next_message = "Ok, what is your review?"
        next_stage = "GiveReview"
    bot.send_message(User.id, next_message)
    setUserContextAndStage(User.id, next_context, next_stage)
    

def ScoreFilmResponse(bot, message, User):
    """Stage 5 Response. Checks whether the user entered a score between 1-5, and if so,
    stores it in the database.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    next_stage = stages['filmReview']['ScoreFilm']
    next_message = "Sorry I'm not sure I understand. Could you enter a score for the film out of 5? 1 being poor and 5 being excellent."
    next_context = contexts['FilmReview']
    try:
        score = round(float(message))
        liked = db.getReview(User.id, User.suggested_film)['Pos']
        db.insertUserRating(User.id, User.suggested_film, liked, score)
        db.removeSuggestedFilm(User.id)
        next_stage = User.previous_stage
        next_context = User.previous_context
        next_message = "Excellent! Thank you for rating the film."
    except Exception as e:
        print("Error rounding user rating", str(e))
    bot.send_message(User.id, next_message)
    setUserContextAndStage(User.id, next_context, next_stage)


def filmReviewHandler(bot, update, User):
    """Handler function to call the relevant function depending on
    what stage the user is on in the film review journey.
    @param {Bot} bot
    @param {String} message
    @param {Person} User"""
    message = update.message.text
    if User.stage == 1:
        AskIfWatchedResponse(bot, message, User)
    elif User.stage == 2:
        AskReviewResponse(bot, message, User)
    elif User.stage == 3:
        GiveReviewResponse(bot, message, User)
    elif User.stage == 4:
        ConfirmNoReviewResponse(bot, message, User)
    elif User.stage == 5:
        ScoreFilmResponse(bot, message, User)