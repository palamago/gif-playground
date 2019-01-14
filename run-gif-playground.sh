#!/bin/sh
if ! pgrep -fl "run-gif-playground.sh" > /dev/null
then
    echo "Running !"
else
	cd /var/www/bots/gif-playground
    python gif_bot.py
fi