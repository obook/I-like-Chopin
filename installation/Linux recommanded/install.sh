#!/bin/sh

printf 'Install I-Like-Chopin (y/n)? '
read answer
if  [ "$answer" = "Y" ] || [ "$answer" = "y" ] ; then
    # Program
    rm -R ../../src/__pycache__ 2> /dev/null
    sudo mkdir -p /usr/share/i-like-chopin/icons
    sudo cp ../../src/*.py /usr/share/i-like-chopin
    sudo cp -r ../../src/icons /usr/share/i-like-chopin
    sudo cp -r ../../src/ui /usr/share/i-like-chopin
    sudo cp bin/i-like-chopin-poetry /usr/bin/i-like-chopin

    # Midifile
    cp -r ../../src/midi ~/.local/share/i-like-chopin

    # Icons
    sudo cp ../../src/icons/32x32/i-like-chopin.png /usr/share/icons/hicolor/32x32/apps
    sudo cp ../../src/icons/svg/i-like-chopin.svg /usr/share/icons/hicolor/scalable/apps

    # Desktop
    sudo cp desktop/org.obook.i-like-chopin.desktop /usr/share/applications

    echo Done
    exit
fi

echo Aborted

: <<'FUTUR_USE'
printf 'Install I-Like-Chopin (y/n)? '
read answer
if  [ "$answer" = "Y" ] || [ "$answer" = "y" ] ; then
    printf 'System or Poetry (s/p)? '
    read answer
    if  [ "$answer" = "S" ] || [ "$answer" = "s" ] ; then
        echo Installation on system Done
        exit 0
    fi
    if  [ "$answer" = "P" ] || [ "$answer" = "p" ] ; then
        echo Installation with poetry Done
        exit 0
    fi

fi

echo Aborted
FUTUR_USE
