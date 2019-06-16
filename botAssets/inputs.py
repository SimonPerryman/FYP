"""

Inputs file

Predefined expected inputs, used for the "check for expected input" functionality
to predict whether a user is using a synonym of a word or phrase.

All expected inputs have been passed through the lemmatize_sentence function in
the nlp_techniques/preprocessing.py file.

"""

greetings = [
    "hi",
    "hello",
    "hey",
    "sup",
    "whats up",
    "what is up",
    "how you doing",
    "yo"
]

positives = [
    "ok",
    "that be correct",
    "correct",
    "sure",
    "great",
    "yes",
    "sound good",
    "perfect",
    "yeah",
    "excellent"
]

negatives = [
    "no",
    "wrong",
    "i do not want this"
]

negative_film_responses = [
    "i do not like this",
    "i want a different",
    "i be not a fan of this",
    "i have see this",
    "do not want to see this"
]

skip = [
    "skip",
    "i want to skip this",
    "i do not care"
]

feeling = [
    "how be -PRON-",
    "be -PRON- alright",
    "alright",
    "how -PRON- do",
    "-PRON- ok"
]

cancel = [
    "i want to cancel",
    "i do not want to do this anymore",
    "stop",
    "exit",
    "leave"
]