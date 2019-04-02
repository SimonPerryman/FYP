# Default Python Packages
import logging
import random
import time
from configparser import ConfigParser

# Third Party Libraries
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

# Program Files
from database import insertUser, newConversation
import conversations
import botAssets
import commands

config = ConfigParser()
config.read("./config/config.ini")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=config.getint("settings", "logging_level"))
                    
def start(bot, update):
    insertUser(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name)
    newConversation(update.message.chat.id, {
        "MessageID": random.randint(0, 99999999),
        "Message": update.message.text,
        "Timestamp": int(time.time())
    })
    genres_keyboard = botAssets.genresKeyboard()
    reply_markup = telegram.ReplyKeyboardMarkup(genres_keyboard)
    bot.send_message(chat_id=update.message.chat_id, 
                    text="""Hey {}! Thanks for talking to me, I haven't spoken to anyone in a while! I'm really interested in films.
                    My favourite genre is comedy, what's yours?""".format(update.message.chat.first_name), 
                    reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
update_genre_handler = CommandHandler('ufg', commands.updateGenre, pass_args=True)
greetings_handler = MessageHandler(botAssets.GreetingFilter(), conversations.greetings)
conversation_handler = MessageHandler(Filters.text, conversations.conversation_handler)
echo_handler = MessageHandler(Filters.text, conversations.echo)

def main():
    updater = Updater(token=config.get("bot", "token"))
    dispatcher = updater.dispatcher

    # Commands
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(update_genre_handler)
    
    # Strict Messages
    dispatcher.add_handler(greetings_handler)

    # Conversation Handler
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    # updater.idle()
    print("Started Bot")

if __name__ == "__main__":
    main()