from telegram.ext import BaseFilter
from inputs import greetings

class TestFilter(BaseFilter):
    def filter(self, message):
        return 'test123' in message.text

class GreetingFilter(BaseFilter):
    def fitler(self, message):
        return message.text.lower() in greetings