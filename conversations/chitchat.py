from random import randint
import botAssets

def greetingsMessage(bot, update):
  """Greetings message - sends a message with a random greeting"""
  message = "{} {}!".format(botAssets.inputs.greetings[randint(0, (len(botAssets.inputs.greetings) - 1))].capitalize(), update.message.chat.first_name)
  bot.send_message(chat_id=update.message.chat_id, text=message)

def moodMessage(bot, update):
  """Feelings/Mood message - "how are you" response """
  bot.send_message(chat_id=update.message.chat_id, text=botAssets.get_mood())