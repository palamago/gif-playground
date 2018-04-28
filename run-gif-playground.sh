#!/bin/sh
if ! pgrep -fl "run-gif-playground.sh" > /dev/null
then
    echo "Running !"
else
    python gif_bot.py
fi