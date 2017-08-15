#!/bin/bash

# Note: 3.6+ is required for discord.py
PYTHON="python3.6"

# Enter wherever you place your downloaded dir
BOT_DIR="$HOME/TapeKvlt-Discord-Bot"

cd $BOT_DIR && git pull && $PYTHON bot.py &
