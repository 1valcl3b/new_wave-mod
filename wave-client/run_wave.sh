#!/bin/bash

PATH_LOADGEN="/home/vlc/loadgen"
TARGET="http://server/video.mp4"

Help()
{
   # Display Help
   echo "Syntax: run_wave.sh [-l|h|V]"
   echo "options:"
   echo "-l     load model."
   echo "-h     Print this Help."
   echo "-V     Print software version and exit."
   echo
}

if [ $1 == "-l" ]; then
    if [ $2 == "sinusoid" ]; then
    
        A=$3 #Amplitude
        P=$4 #Period
        D=$5 #Duration
        L=$6 #Lambd

        touch /home/vlc/logs/sinusoid_wave.csv
        chmod 666 /home/vlc/logs/sinusoid_wave.csv

        #Run sinusoid loadGen model    
        python3 $PATH_LOADGEN/$2/$2.py -s $A,$P $D $L -l $TARGET
    
    fi
    if [ $2 == "flashcrowd" ]; then

        Rnorm=$3 #Normal load
        S=$4 #Shock Level
        n=$5 #Constant from rampdown

        touch /home/vlc/logs/flashcrowd_wave.csv
        chmod 666 /home/vlc/logs/flashcrowd_wave.csv
    
        #Run flashcrowd loadGen model    
        python3 $PATH_LOADGEN/$2/$2.py -f $Rnorm,$S,$n -l $TARGET

    fi
    if [ $2 == "stair_step" ]; then
    
        I=$3 #Interval
        J=$4 #Jump
        D=$5 #Duration

        touch /home/vlc/logs/stair_step_wave.csv
        chmod 666 /home/vlc/logs/stair_step_wave.csv

        #Run stair_step loadGen model
        python3 $PATH_LOADGEN/$2/$2.py -s $I,$J $D -l $TARGET
    
    fi
fi
if [ $1 == "-h" ]; then
    Help
fi
