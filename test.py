import os
from environment_variables import add_environment_variables
from misc import save_pickle, load_pickle
import nltk.tokenize
def test():
  add_environment_variables()
  print(os.environ['PICKLE_DIRECTORY'])
  return True

if __name__ == '__main__':
  test()
