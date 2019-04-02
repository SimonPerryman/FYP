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
        
    },
    "ChitChat": 1,
    "Error": 0
}


def getStage(context):
    return {
        1: "registrationStages"
    }.get(context, '')


# Ensure No Stages/Contexts are 0 as that is the error state.