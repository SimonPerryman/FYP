from database import getAllGenres

def genresKeyboard():
    genres = getAllGenres()
    custom_keyboard = []
    for x in range(0, 7):
        row = []
        for i in range(0,4):
            pos = (x * 4) + i
            row.append(genres[pos]['Name'])
        custom_keyboard.append(row)
    custom_keyboard.append(["Skip this for now!"])

    return custom_keyboard

def scoreKeyboard():
    return [["1", "2", "3", "4", "5"]]