#!/usr/bin/env bash

# ./start-api.sh

if command -v pacman &> /dev/null; then
   # Arch Linux
   if ! python3 -m venv --help &> /dev/null; then
      echo -e "❌  Python venv module is not available. Install it using:\n"
      echo "sudo pacman -S python"
      exit 1
   fi
elif command -v dpkg &> /dev/null; then
   # Debian-based systems
   dpkg --list | grep "python3-venv" > /dev/null

   if [ $? -ne 0 ]; then
      echo -e "❌  Package python3-venv is not installed! Install it using:\n"
      echo "sudo apt install python3-venv"
      exit 1
    fi
fi

if [ -d venv ]; then

   echo -e "🐍  Activating Python virtual environment... "
   source venv/bin/activate
   pip3 freeze | grep -E "flask-restx" > /dev/null
   if [ ! $? -ne 0 ]; then
      echo "📦  Installing API dependencies... "
      pip3 install flask flask-restx python-dotenv requests > /dev/null
   fi
else
   echo "🕒 Creating Python virtual environment... "
   python3 -m venv venv
   echo -e "🐍  Activating Python virtual environment... "
   source venv/bin/activate

   echo "📦  Installing API dependencies... "
   pip3 install flask flask-restx python-dotenv requests > /dev/null
fi

echo -e "🔛  Start API in port 8181\n"
python3 api/api.py
