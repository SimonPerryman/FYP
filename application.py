import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
import telegram
import database
import conversations
import botAssets
import commands
from configparser import ConfigParser
import random
import time

config = ConfigParser()
config.read("./config/config.ini")

logging.basicConfig(format=config.get("settings", "logging_format"), level=config.getint("settings", "logging_level"))
                    
def start(bot, update):
    database.insertUser(update.message.chat.id, update.message.chat.FirstName, update.message.chat.lastName)
    database.newConversation(update.message.chat.id, {
        "MessageID": random.randint(0, 99999999),
        "Message": update.message.text,
        "Timestamp": int(time.time())
    })
    # genres = dbcall.getGenres()
    custom_keyboard = [['genres'], ['Skip this for now!']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, 
                    text="Custom Keyboard Test", 
                    reply_markup=reply_markup)
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
update_genre_handler = CommandHandler('ufg', commands.updateGenre, pass_args=True)

def main():
    updater = Updater(token=config.get("bot", "token"))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(update_genre_handler)
    # dispatcher.add_handler(echo_handler)
    # dispatcher.add_handler(caps_handler)
    # dispatcher.add_handler(keyboard_handler)
    updater.start_polling()
    updater.idle()
    print("Started Bot")

if __name__ == "__main__":
    main()