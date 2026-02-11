#!/bin/bash

set -e

# PID_FILE="/tmp/wave_mininet.pid"

# if [ -f "$PID_FILE" ]; then
#     sudo kill $(cat $PID_FILE) || true
#     rm -f $PID_FILE
# fi

sudo mn -c  >/dev/null 2>&1

sudo rm -f /tmp/ultimo_switch.txt

echo "[WAVE] Mininet stopped"

