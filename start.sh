#!/bin/sh

TOKEN="$(cat ./token.txt)"

while true ; do

    git pull

    pgrep python3.6 > /dev/null && killall python3.6
    
    python3.6 bot.py $TOKEN

    echo "-------------------------------"
    echo "        Restarting..."
    echo "-------------------------------"

done
