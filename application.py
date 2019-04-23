from environment_variables import add_environment_variables
add_environment_variables()

# Default Python Packages
import logging
import random
import os
from time import time

# Third Party Libraries
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

# Program Files
from database import insertUser, newConversation
import conversations
import botAssets
import commands

logging.basicConfig(format=os.environ['LOGGING_FORMAT'], level=int(os.environ['LOGGING_LEVEL']))
                    
start_handler = CommandHandler('start', conversations.start)
update_genre_handler = CommandHandler('ufg', commands.updateGenre, pass_args=True)
conversation_handler = MessageHandler(Filters.text, conversations.conversation_handler)

def main():
    updater = Updater(token=os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    import datetime
    # Job Queue
    job_queue = updater.job_queue
    job_queue.run_daily(conversations.ask_for_film_review, datetime.time(9, 0))
    job_queue.run_daily(botAssets.calculate_mood, datetime.time(0, 1))

    # Commands
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(update_genre_handler)
    
    # Conversation Handler
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    # updater.idle()
    print("Started Bot")

if __name__ == "__main__":
    main()