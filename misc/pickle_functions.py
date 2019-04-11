import pickle

def load_pickle(name):
    pkl_file = open(name, 'rb')
    loaded_file = pickle.load(pkl_file)
    pkl_file.close()
    return loaded_file

def save_pickle(obj, name):
    output = open(name, 'wb')
    pickle.dump(obj, output)
    output.close()