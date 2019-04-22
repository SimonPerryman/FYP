import os
os.environ['APPLICATION_PATH'] = r"C:/dev/projects/university/FYP/"
from nlp_techniques import lemmatize_sentence
def test():
  messages = [
    "I want to cancel",
    "I don't want to do this anymore",
    "stop",
    "exit",
    "leave"
  ]
  for m in messages:
    print(lemmatize_sentence(m))
  return True

if __name__ == '__main__':
  test()
