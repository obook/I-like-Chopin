#!/bin/bash
# Use only bash, not sh
# Author : obooklage
# Date : 23/01/2025
# Desc1 : check names compatibles for Windows
# Desc2 : create music score from midifiles
# A venv must be created with libraries : mido python-rtmidi

midipath=$HOME"/Documents/GitHub/midi/"

venv_path=$HOME"/PythonEnv/mido"
venv_activate=$venv_path"/bin/activate"
venv_python3=$venv_path"/bin/python3"

# update midilib
/usr/bin/git pull $midipath

# Activate venv
source $venv_activate

# Check filenames
cd ~/Documents/GitHub/I-like-Chopin/tools
$venv_python3 rename-windows.py $midipath

# Make music scores
cd ~/Documents/GitHub/I-like-Chopin/tools/song-score
$venv_python3 song-score-scan.py $midipath

# Deactivate venv
deactivate
