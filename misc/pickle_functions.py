import pickle
import os

def load_pickle(name):
    directory = "{}/{}".format(os.environ['PICKLE_DIRECTORY'], name)
    pkl_file = open(directory, 'rb')
    loaded_file = pickle.load(pkl_file)
    pkl_file.close()
    return loaded_file

def save_pickle(obj, name):
    directory = "{}/{}".format(os.environ['PICKLE_DIRECTORY'], name)
    output = open(directory, 'wb')
    pickle.dump(obj, output)
    output.close()