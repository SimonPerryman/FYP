#!/bin/bash

sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install scikit-surprise
sudo python3 -m spacy download en_core_web_sm
sudo python3 -m spacy download en_core_web_lg
sudo source /opt/python/current/env
sudo python3 application.py