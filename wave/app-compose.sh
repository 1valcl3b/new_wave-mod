#!/usr/bin/env bash
# ./app-compose.sh <option>[--start|--destroy]

OPTION=$1

if command -v ip &> /dev/null; then
  IP=$(ip route get 1.1.1.1 | awk '{print $7}')
elif [ -f /etc/os-release ]; then
    source /etc/os-release
    if [[ "$ID" == "arch" ]]; then
        IP=$(hostname -i | awk '{print $1}')
    else
        IP=$(hostname -I | awk '{print $1}')
    fi
else
    echo "Unable to detect the operating system. Please check your setup."
    exit 1
fi
echo "IP_HOST_API=$IP" > ./.env

ENVFILE=$PWD/.env
if [ ! -s "$ENVFILE" ]; then
        echo "File .env does not exist or is empty!"; exit
fi

case $OPTION in
        "--start")
                # if [ ! -f /etc/vbox/networks.conf ]; then
                #     # Allow all IP ranges to be used in VM creation
                #     sudo mkdir /etc/vbox/
                #     echo '* 0.0.0.0/0 ::/0' | sudo tee /etc/vbox/networks.conf > /dev/null
                # fi

                #echo -e '📺  Activating xhost ...'
                #xhost +local:* > /dev/null
                echo -e '🐳  Building containers ...'
                docker compose build > /dev/null
                echo -e '🐳  Starting containers ...'
                docker compose up -d > /dev/null
                echo -e '🚀  container started successfully!'
                docker pull ghcr.io/ifpb/new_wave/wave-vlc
                docker pull ghcr.io/ifpb/new_wave/wave-apache
                echo "🕒 Initilize API Provision ... "
                bash start-api.sh
                ;;
        "--destroy")
                echo -e '🔴  Destroying containers and images ...'
                docker compose down --rmi all
                docker rmi -f ghcr.io/ifpb/new_wave/wave-vlc ghcr.io/ifpb/new_wave/wave-apache > /dev/null
                cd app/provision
                rm ./logs/* > /dev/null 2>&1
                vagrant destroy -f > /dev/null
                echo "" > .env
                #xhost -local:* > /dev/null
                echo -e '🤝  Finished environment ...'
                ;;
        *)
                echo "Not a valid argument!"
                echo "excution example: ./app-compose.sh <option>[--start|--destroy]"
esac
