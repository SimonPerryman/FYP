#!/bin/bash

app="/opt/python/current/app"
target_dir="/opt/python/run/venv/lib/python3.6/dist-packages"
python -m pip install --upgrade pip --target $target_dir
python -m pip install -r $app/requirements.txt --target $target_dir
python -m pip install scikit-surprise --target $target_dir
python -m spacy download en_core_web_sm --target $target_dir
python -m spacy download en_core_web_lg --target $target_dir
python $app/application.py