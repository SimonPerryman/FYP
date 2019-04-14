# Default Python Packages
import logging
import random
from time import time
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
                    
start_handler = CommandHandler('start', conversations.start)
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