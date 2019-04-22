#!/bin/bash

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install scikit-surprise
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
env_var=$(sed -e 's/export //' -e 's/"//g' /opt/python/current/env)
$env_var python application.py