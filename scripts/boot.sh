cd ~/bank-of-brobots-bot

pipenv run gunicorn -w 4 app:app
