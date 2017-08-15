#!/bin/bash

# Note: 3.6+ is required for discord.py
PYTHON="python3.6"

# Enter wherever you place your downloaded dir
BOT_DIR="$HOME/TapeKvlt-Discord-Bot"

git pull && $PYTHON $BOT_DIR/bot.py
