import database

def isGenre(query):
    #return is in
    return True

def getGenreID(genre):
    #db call
    return 1

def updateGenre(bot, update, args):
    if len(args) == 2 and (args[0] == "1" or args[0] == "2" or args[0] == "3") and isGenre(args[1]):
            favouriteGenreID = 0
            secondFavouriteGenreID = 0
            thirdFavouriteGenreID = 0
            updateField = ""

            if args[0] == "1":
                favouriteGenreID = getGenreID(args[1])
                updateField = "Favourite"
            elif args[0] == "2":
                secondFavouriteGenreID = getGenreID(args[1])
                updateField = "Second Favourite"
            elif args[0] == "3":
                thirdFavouriteGenreID = getGenreID(args[1])
                updateField = "Third Favourite"

            database.updateFavouriteGenres(update.message.chat_id, favouriteGenreID, secondFavouriteGenreID, thirdFavouriteGenreID)
            bot.send_message(chat_id=update.message.chat_id, text="I have updated your {1} genre to be {2}".format(updateField, args[1].capitalize()))
    else:
        bot.send_message(chat_id=update.message.chat_id, 
        text="""Sorry, you have entered the command wrong! Please type a number between
        1-3 then the genre you wish to change to, for example '/ufg 1 Comedy'""")

def listFavouriteGenres(bot, update):
    # just do a DB call and then output the results.
    return 0
