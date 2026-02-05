#!/bin/bash

PATH_LOADGEN="/home/vlc/loadgen"

Help()
{
   # Display Help
   echo "Syntax: run_microburst.sh [-l|-h]"
   echo "options:"
   echo "-l     load microburst."
   echo "-h     Print this Help."
   echo
}

if [ $1 == "-l" ]; then
    IP=$2
    DURATION=$3

    python3 $PATH_LOADGEN/microburst/microburst.py -d $IP $DURATION
fi
if [ $1 == "-h" ]; then
    Help
fi
