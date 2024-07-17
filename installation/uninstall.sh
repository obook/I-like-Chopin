#!/bin/sh

printf 'Uninstall I-Like-Chopin (y/n)? '
read answer

if [ "$answer" = "${answer#[Yy]}" ] ;then

    # Program
    sudo rm -R /usr/share/i-like-chopin 2> /dev/null
    sudo rm -R /usr/bin/i-like-chopin 2> /dev/null

    # Midifile
    # rm -R ~/.local/share/i-like-chopin 2> /dev/null

    # Icons
    sudo rm /usr/share/icons/hicolor/32x32/apps/i-like-chopin.png
    sudo rm /usr/share/icons/hicolor/scalable/apps/i-like-chopin.svg

    # Desktop
    sudo rm /usr/share/applications/org.obook.i-like-chopin.desktop

    # Config
    rm ~/.config/i-like-chopin.json

    echo Done

else
    echo Aborted
fi
