from .users import (insertUser, getUser, setUserContext, setUserStage, setLastMessage)
from .conversations import (addToConversation, newConversation, getUserConversations,
                            getSpecificUserConversation)
from .genres import (getGenre, getAllAlternativeGenreNames, getGenreByAlternativeGenreName,
                    updateFavouriteGenres, getFavouriteGenres, getSpecificFavouriteGenre,
                    insertFavouriteGenres, getAllGenres)

# from .db_connection import connect