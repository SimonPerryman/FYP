import os
def test():
  print("hello", os.path.dirname(os.path.realpath(__file__)))
  
  return True

if __name__ == '__main__':
  test()
