#!/bin/bash

# Check if the bot.py process is currently running
if pgrep -f "python3 bot.py" >/dev/null; then
    # If running, kill the process
    echo "Bot is currently running."
else
    # If not running,
    echo "Bot is not running."
fi

