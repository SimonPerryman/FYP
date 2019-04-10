#TODO Fill this out
# Previous Context
contexts = {
    "Error": 0,
    "InitialUserRegistration": 1,
    "FilmSuggestion": 2,
    "ChitChat": 3
}

stages = {
    "registrationStages": {
        "Error": 0,
        "FirstGenre": 1,
        "SecondGenre": 2,
        "ThirdGenre": 3,
        "Age": 4
    },
    "filmSuggestion": {
        "Error": 0,
        "InitialQuery": 1,
        "ConfirmFilm": 2,
        "AskFilm": 3,
        "ConfirmGenre": 4,
        "AskGenre": 5,
        "ConfirmCrew": 6,
        "AskCrew": 7,
        "SuggestedFilm": 8 
    },
    "ChitChat": 1,
    "Error": 0
}


def getStage(context):
    return {
        1: "registrationStages",
        2: "filmSuggestion"
    }.get(context, '')


# Ensure No Stages/Contexts are 0 as that is the error state.