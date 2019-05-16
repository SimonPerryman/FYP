import os
import sys
from time import time
from random import randint
sys.path.insert(0, os.environ['APPLICATION_PATH'])
import database as db

def calculate_mood():
  """Calculates mood based on the amount of users 
  who have messaged the chatbot in the past day."""
  print("Updating happiness points, current points:", os.environ['BOT_HAPPINESS'])
  currentTime = time()
  users = db.getAllUsers()
  num_users = len(users)
  spoken_to_recently = 0
  for user in users:
    if user['LastMessage'] - currentTime < 86400:
      spoken_to_recently += 1
    
  active_users = spoken_to_recently / num_users
  happiness = int(os.environ.get('BOT_HAPPINESS', 0))
  if active_users >= 0.75:
    print("75 percent or more users spoke to chatbot, increasing points by 1")
    happiness += 1
  elif active_users >= 0.25 and active_users < 0.5:
    print("between 25 percent and 50 percent of users spoke to chatbot, decreasing points by 1")
    happiness -= 1
  elif active_users < 0.25:
    print("Fewer than 25 percent of users spoke to chatbot, setting points to 0")
    happiness = 0

  print("New happiness points:", happiness)
  os.environ['BOT_HAPPINESS'] = str(happiness)

def get_mood():
  """Uses the bots happiness to figure out how it is feeling today.
  @returns {String} message"""
  happiness = int(os.environ['BOT_HAPPINESS'])
  responses = ["Today isn't my day", "I'm feeling miserable", "I'm very upset"] 
  
  if happiness >= 3:
    responses = ["I'm feeling amazing thanks", "I'm really happy right now.", "I'm feeling great", "I'm feeling on top of the world!"]
  elif happiness == 2:
    responses =  ["I'm ok", "I'm feeling alright thanks", "I'm not bad"]
  elif happiness <= 1:
    responses = ["I'm feeling not the best", "I'm a bit lonely", "I've been better"]

  index = randint(0, len(responses) - 1)
  return responses[index]