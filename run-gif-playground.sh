#!/bin/bash
#Check if is running
if ! pgrep -fl "run-gif-playground.sh" > /dev/null
then
    python gif_bot.py
fi