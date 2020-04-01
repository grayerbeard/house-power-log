#!/bin/bash
cd /home/pi/house-power-log
echo looking to kill any existing power-log session
tmux kill-session -t power-log
echo now new tmux power-log session
tmux new-session -d -s power-log 'python3 house-power.py'
