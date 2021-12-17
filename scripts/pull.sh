cd ~/bank-of-brobots-bot

git reset --hard
git clean -f -d
git pull

pipenv install --deploy

cp scripts/bot.service ~/.config/systemd/user/bank-of-brobots-bot.service
systemctl --user daemon-reload
systemctl --user restart bank-of-brobots-bot.service
