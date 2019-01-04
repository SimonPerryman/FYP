from pymongo import MongoClient
from configparser import ConfigParser
import random

config = ConfigParser()
config.read("../config/config.ini")

client = MongoClient()

# db = client[config.get("Mongo_db", "db_name")]
# conversations_collection = db[config.get("Mongo_db", "conversations_collection")]
db = client['testing']
conversations_collection = db['conversations']

def addToConversation(UserID, ConversationID, MessageID, Text, Timestamp):
    return conversations_collection.update({
        "UserID": UserID,
        "Conversation.ConversationID": ConversationID
    }, {
        "$push": {
            "Conversations.$.Conversation": {
                "MessageID": MessageID,
                "Message": Text,
                "Timestamp": Timestamp
            }
        }
    })

def newConversation(UserID, Conversation):
    return conversations_collection.update({
        "UserID": UserID
    }, {
        "$push": {
            "ConversationID": random.randint(0, 99999999),
            "Conversation": Conversation
        }
    })

def getUserConversations(UserID):
    return conversations_collection.find_one({
        "UserID": UserID
    }, projection={"Conversations": 1})

def getSpecificUserConversation(UserID, ConversationID):
    return conversations_collection.find_one({
        "UserID": UserID,
        "Conversations.ConversationID": ConversationID
    }, {
        "Conversations.$.Conversation": 1
    })

# newConversation("1231", )