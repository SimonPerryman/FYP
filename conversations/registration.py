import telegram
from context import stages, contexts
from database import getAllGenres, insertFavouriteGenres, setUserContextAndStage, updateUserAge
from .errors import errorMessage

def askSecondFavouriteGenre(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Awesome. What's your next favourite genre?! Mine's Superhero films :)")

def askThirdFavouriteGenre(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sweet. What's your third favourite genre?! If I had to guess I'd say you like horror films!")

def askAge(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Nice. I like also like <X>! I guess I just love all types of films!")
    bot.send_message(chat_id=update.message.chat_id, text="It's my birthday tomorrow. I'm going to be 22. How old are you?",
                    reply_markup=telegram.ReplyKeyboardRemove())

def askAgeAgain(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't quite understand? How old are you?")
    bot.send_message(chat_id=update.message.chat_id, text="If you don't want to let me know, just say \"skip\".")
 
def registrationComplete(bot, update):
    if(int(update.message.text) < 18):
        bot.send_message(chat_id=update.message.chat_id, text="Noted. I won't suggest anything that is innapropriate for your age")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Excellent. I will suggest all types of film")
    bot.send_message(chat_id=update.message.chat_id, text="I've collected everything I need to. What can I do for you today?")
    # TODO Custom Keyboard maybe    

def skipResponse(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="""Sorry, I thought I was being a bit too <X> myself. If you want to tell me your
                                                            favourite genres later just let me know, but for now I'll just try to figure it out myself haha""",
                    reply_markup=telegram.ReplyKeyboardRemove())

def registrationHandler(bot, update, User):
    message = update.message.text
    messageLower = message.lower()
    if "skip" in messageLower:
        skipResponse(bot, update)
        setUserContextAndStage(User.id, contexts['ChitChat'], stages['ChitChat'])
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
                setUserContextAndStage(User.id, User.context, stages['registrationStages']['SecondGenre'])
                askSecondFavouriteGenre(bot, update)
            elif User.stage == stages['registrationStages']['SecondGenre']:
                insertFavouriteGenres(User.id, 0, genreID, 0)
                setUserContextAndStage(User.id, User.context, stages['registrationStages']['ThirdGenre'])
                askThirdFavouriteGenre(bot, update)
            elif User.stage == stages['registrationStages']['ThirdGenre']:
                insertFavouriteGenres(User.id, 0, 0, genreID)
                setUserContextAndStage(User.id, User.context, stages['registrationStages']['Age'])
                askAge(bot, update)
        elif User.stage == stages['registrationStages']['Age']:
            if message.isdigit() and int(message) in range(4,100):
                updateUserAge(User.id, int(message))
                setUserContextAndStage(User.id, contexts['ChitChat'], stages['ChitChat'])
                registrationComplete(bot, update)
            else:
                askAgeAgain(bot, update)
        else:
            errorMessage(bot, update)