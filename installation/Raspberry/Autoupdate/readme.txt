Get MidiLib
-----------
/usr/bin/git clone https://github.com/obook/midi.git /home/<username>/.local/share/i-like-chopin/midi

Auto update
+++++++++++

Edit crontab (crontab -e) and add (adjust 15 seconds delay as you wich):

Auto update Main program
------------------------
@reboot sleep 15 && /usr/bin/git -C /home/<username>/<yourpath>/I-like-Chopin pull

Auto update MidiLib
-------------------
@reboot sleep 15 && /usr/bin/git -C /home/<username>/.local/share/i-like-chopin/midi pull
