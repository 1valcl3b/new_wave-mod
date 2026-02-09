#!/bin/bash

set -e

TOPOLOGY=$1
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROVISION_DIR="$BASE_DIR"

PID_FILE="/tmp/wave_mininet.pid"
LOG_FILE="/tmp/wave_mininet.log"
SWITCH_FILE="/tmp/ultimo_switch.txt"

echo "[WAVE] Starting Mininet topology: $TOPOLOGY"

sudo mn -c  >/dev/null 2>&1

if [ -f "$PID_FILE" ]; then
    sudo kill $(cat $PID_FILE) || true
    rm -f $PID_FILE
fi

case "$TOPOLOGY" in
    tree)
        SCRIPT="net-tree.py"
        ;;
    linear)
        SCRIPT="net-linear.py"
        ;;
    *)
        echo "Invalid topology"
        exit 1
        ;;
esac


# echo "[DEBUG] PROVISION_DIR=$PROVISION_DIR"
# echo "[DEBUG] SCRIPT=$SCRIPT"
# ls -l "$PROVISION_DIR/$SCRIPT"

sudo python3 "$PROVISION_DIR/$SCRIPT" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

echo "[WAVE] Waiting ultimo_switch.txt..."

while [ ! -f "$SWITCH_FILE" ]; do
    sleep 1
done

LAST_SWITCH=$(cat "$SWITCH_FILE")

sudo ip link set s1 up || true
sudo ip link set "$LAST_SWITCH" up || true

echo "[WAVE] Mininet ready"

