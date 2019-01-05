from database import getAllGenres
from botAssets import genresKeyboard
import telegram
i = 0
def wip_function(bot, update):
    if i == 0:
        # genres = getAllGenres()
        # custom_keyboard = []
        # for x in range(0, 7):
        #     row = []
        #     for i in range(0,4):
        #         pos = (x * 4) + i
        #         row.append(genres[pos]['Name'])
        #     custom_keyboard.append(row)
        # custom_keyboard.append(["Skip this for now!"])
        # # for x in range(0, 7):
        # #     row = []
        # #     start = 4*x
        # #     finish = (4 * (x + 1)) - 1
        # #     row.append(genres[start:finish])
        # #     custom_keyboard.append(row)
        # # custom_keyboard.append(["Skip this for now!"])

        # print(custom_keyboard)

        # # custom_keyboard = [["hi"], ["ok"]]

        reply_markup = telegram.ReplyKeyboardMarkup(genresKeyboard())

        bot.send_message(chat_id=update.message.chat_id, 
                    text="wip Function Message", 
                    reply_markup=reply_markup)
        i+= 1
    else:
        telegram.ReplyKeyboardRemove()