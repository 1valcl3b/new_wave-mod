#!/bin/bash

STATUS_FILE="/home/vlc/logs/ready.txt"

sleep 2

echo "container ready" > "$STATUS_FILE"

tail -f /dev/null