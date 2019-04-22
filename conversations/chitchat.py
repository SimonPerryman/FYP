from random import randint
import botAssets

def test():
    return "Test"

def greetings(bot, update):
    message = "{} {}!".format(botAssets.inputs.greetings[randint(0, (len(botAssets.inputs.greetings) - 1))].capitalize(), update.message.chat.first_name)
    bot.send_message(chat_id=update.message.chat_id, text=message)

def feelings(bot, update):
    print("#TODO Should put something like CRON job to figure how the bot is doing. If few people have spoke to the bot, it gets sadder.")