#!/bin/bash

TOKEN=$(cat token.txt)

while true ; do

    git pull

    killall python3.6 ||
        pkill -9 python3.6
    
    python3.6 bot.py $TOKEN

    echo "-------------------------------"
    echo "        Restarting..."
    echo "-------------------------------"

done
