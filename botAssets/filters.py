from telegram.ext import BaseFilter
from .inputs import greetings

class wipFilter(BaseFilter):
    def filter(self, message):
        return message.text.lower() == "test"

class GreetingFilter(BaseFilter):
    def filter(self, message):
        return message.text.lower() in greetings