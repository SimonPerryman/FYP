import re

def getGenre(genre):
    return {
        'action': 1,
        'adult': 2,
        'adventure': 3,
        'animation': 5,
        'biography': 6,
        'comedy': 7,
        'crime': 8,
        'documentary': 9,
        'drama': 10,
        'family': 11,
        'fantasy': 12,
        'film-noir': 13,
        'game-show': 14,
        'history': 15,
        'horror': 16,
        'music': 17,
        'musical': 18,
        'mystery': 19,
        'news': 20,
        'romance': 21,
        'sci-fi': 22,
        'short': 23,
        'sport': 24,
        'superhero': 25,
        'talk-show': 26,
        'thriller': 27,
        'war': 28,
        'western': 29
    }.get(genre, None)

def preprocess_string(string):
    return re.sub(r"[^\s^\d^\w]", "", string.lower()).replace(" ", "")