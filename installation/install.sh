#!/bin/sh

# Program
rm -R ../src/__pycache__ 2> /dev/null
sudo mkdir -p /usr/share/i-like-chopin/icons
sudo cp ../src/*.py /usr/share/i-like-chopin
sudo cp -r ../src/icons /usr/share/i-like-chopin
sudo cp -r ../src/template /usr/share/i-like-chopin
sudo cp bin/i-like-chopin /usr/bin

# Midifile
cp -r ../src/midi ~/.local/share/i-like-chopin

# Icons
sudo cp ../src/icons/32x32/i-like-chopin.png /usr/share/icons/hicolor/32x32/apps
sudo cp ../src/icons/svg/i-like-chopin.svg /usr/share/icons/hicolor/scalable/apps

# Desktop
sudo cp desktop/org.obook.i-like-chopin.desktop /usr/share/applications
