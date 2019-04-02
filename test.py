import spacy
nlp = spacy.load('en_core_web_lg')




def test():
  suggest = [
      "Suggest a better film for me!",
      "What is a good film to watch at the moment",
      "Give me a Steven Spielberg film",
      "Show me a film that steven spielberg directed that i have not seen yet",
      "any film",
      "film", 
      "please can you suggest a comedy",
      "Thanks for that, can you suggest another film",
      "I've seen that one before. Give me another suggestion"
  ]

  Main = nlp(u'Can you suggest a film for me to watch')
  for s in suggest:
    print(Main.similarity(nlp(u'{}'.format(s))))
  return True


if __name__ == '__main__':
  test()