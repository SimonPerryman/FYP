from .chitchat import *
from .films import *
from .registration import *

def filler():
    print(test())
    return False

def echo(bot, update):
    print("update12:", update)
    file = open("Update.text", "w")
    file.write("Update: {}".format(update))
    file.close()
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)