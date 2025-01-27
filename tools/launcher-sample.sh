#!/bin/bash
# Use only bash, not sh
# Author : obooklage
# Date : 27/01/2025
# Desc1 : Update midi library and i-love-chopin
# Desc2 : Launch i-love-chopin and brave web browser

applicationpath=$HOME"/Documents/GitHub/I-like-Chopin"
midipath=$HOME"/Documents/GitHub/midi"
synth=$HOME"/Musique/Pianoteq 8 STAGE/x86-64bit/Pianoteq 8 STAGE"

# update application
cd $applicationpath
/usr/bin/git pull

# update midilib
cd $midipath
/usr/bin/git pull

# Kill the applications that consume too much CPU or too much memory.
killall insync
killall AppRun.wrapped  # NextCloud
killall pcloud

# Launch virtual piano synth
"$synth" &

# Launch i-love-chopin
cd $applicationpath/src
poetry run python i-like-chopin.py &

# Launch brave-browser
sleep 8
/usr/bin/brave-browser "http://127.0.0.1:8888" &

