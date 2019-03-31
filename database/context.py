#TODO Fill this out
# Previous Context
contexts = {
    "Error": 0,
    "InitialUserRegistration": 1
}

stages = {
    "registrationStages": {
        "Error": 0,
        "FirstGenre": 1,
        "SecondGenre": 2,
        "ThirdGenre": 3,
        "Age": 4
    }
}


def getStage(context):
    return {
        1: "registrationStages"
    }.get(context, '')


# Ensure No Stages/Contexts are 0 as that is the error state.