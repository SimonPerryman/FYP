from random import randint
import botAssets

def test():
    return "Test"

def greetings(bot, update):
    message = "{} {}!".format(botAssets.inputs.greetings[randint(0, (len(botAssets.inputs.greetings) - 1))].capitalize(), update.message.chat.first_name)
    bot.send_message(chat_id=update.message.chat_id, text=message)