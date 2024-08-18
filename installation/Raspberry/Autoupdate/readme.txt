Edit crontab (crontab -e) and add (adjust 15 seconds delay as you wich):

@reboot sleep 15 && /usr/bin/git -C /home/<username>/<yourpath>/I-like-Chopin pull
