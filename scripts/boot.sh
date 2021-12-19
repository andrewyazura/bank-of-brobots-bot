#!/bin/bash

cd ~/bank-of-brobots-bot

pipenv run gunicorn -w 4 -b :5001 app:app
