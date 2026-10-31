# FYP - FilmIO
A system composed of a Telegram chatbot that converses about films, a hybrid recommendation system made up of a content-based and collaborative system, and a film review classifier, providing sentiment analysis capabilities.

All files are written in Python, aside from the startup script.

## Dependencies
Python 3.6 must be installed.

`pip install -r requirements.txt`

`pip install scikit-surprise`

`python -m spacy download en_core_web_sm`

`python -m spacy download en_core_web_lg`

## Instructions
In the root directory, run the application.py file

When running locally (no `RDS_HOSTNAME` set), the app connects to a MySQL database `filmio` on `localhost` as `root`. Set the password in the environment first:

`export LOCAL_DB_PASSWORD=<your local MySQL root password>`

The Telegram bot token is read from `BOT_TOKEN`.
