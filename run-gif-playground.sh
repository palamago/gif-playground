#!/bin/bash
if ! pgrep -fl "run-gif-playground.sh" > /dev/null
then
    	echo "Running !"
else
	. .env
	python gif_bot.py
fi
