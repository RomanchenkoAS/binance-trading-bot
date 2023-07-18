#!/bin/bash

# Check if the bot.py process is currently running
if pgrep -f "python3 bot.py" >/dev/null; then
    # If running, kill the process
    echo "Bot is currently running. Stopping..."
    pkill -f "python3 bot.py"
    echo "Bot stopped."
else
    # If not running, start the process
    echo "Bot is not running. Starting..."
    nohup python3 bot.py > nohup.out 2>&1 &
    echo "Bot started."
fi


