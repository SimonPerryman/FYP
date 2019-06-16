"""

Custom filters file

Custom filters for the telegram bot API library.
Currently none in use as all messages go through
the conversation handler rather than using filters.

"""

from telegram.ext import BaseFilter
from .inputs import greetings

class GreetingFilter(BaseFilter):
    def filter(self, message):
        return message.text.lower() in greetings