import spacy
nlp = spacy.load('en_core_web_lg')

def FilmSuggestionHandler(bot, update, User):
  message = update.message.text
  tokenzised = nlp(u'{}'.format(message))
  print(tokenzised)

  print(True)