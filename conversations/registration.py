import telegram
from context import stages
from database import getAllGenres, insertFavouriteGenres, setUserStage
from .errors import errorMessage

def askSecondFavouriteGenre(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Awesome. What's your next favourite genre?! Mine's Superhero films :)")

def askThirdFavouriteGenre(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sweet. What's your third favourite genre?! If I had to guess I'd say you like horror films!")

def askAge(bot, update):
    # Set Context/Stage
    bot.send_message(chat_id=update.message.chat_id, text="Nice. I like also like <X>! I guess I just love all films!")
    bot.send_message(chat_id=update.message.chat_id, text="It's my birthday tomorrow. I'm going to be 22. How old are you?",
                    reply_markup=telegram.ReplyKeyboardRemove())

def skipResponse(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="""Sorry, I thought I was being a bit too <X> myself. If you want to tell me your
                                                            favourite genres later just let me know, but for now I'll just try to figure it out myself haha""",
                    reply_markup=telegram.ReplyKeyboardRemove())

def registrationHandler(bot, update, User):
    message = update.message.text
    messageLower = message.lower()
    if "skip" in messageLower:
        skipResponse(bot, update)
    else:
        genresInfo = getAllGenres()
        genreNames = []
        genreIDs = []
        for individualGenreInfo in genresInfo:
            genreNames.append(individualGenreInfo['Name'])
            genreIDs.append(individualGenreInfo['GenreID'])
        
        if messageLower in genreNames:
            genreID = genreIDs[genreNames.index(messageLower)]
            #TODO Check if the user choices are unique
            #TODO Allow users to change their previous choices in this section
            if User.stage == stages['registrationStages']['FirstGenre']:
                insertFavouriteGenres(User.id, genreID, 0, 0)
                setUserStage(User.id, User.context, stages['registrationStages']['SecondGenre'])
                askSecondFavouriteGenre(bot, update)
            elif User.stage == stages['registrationStages']['SecondGenre']:
                insertFavouriteGenres(User.id, 0, genreID, 0)
                setUserStage(User.id, User.context, stages['registrationStages']['ThirdGenre'])
                askThirdFavouriteGenre(bot, update)
            elif User.stage == stages['registrationStages']['ThirdGenre']:
                insertFavouriteGenres(User.id, 0, 0, genreID)
                setUserStage(User.id, User.context, stages['registrationStages']['Age'])
                askAge(bot, update)
        else:
            errorMessage(bot, update)