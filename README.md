# I like Chopin
Funny program for play like Chopin.
(tribute to Gazebo)

<p align="center">
    <img src="media/20240717_192901.png"  width="600">
</p>

# Description

"I like Chopin" is a very special MIDI player for Linux, Mac or Windows that uses Python3. Any random key pressed on a physical master keyboard plays the correct note from the MIDI file. When all keys are released, the MIDI player stops. You need a physical MIDI master keyboard connected to the computer. The selection of music is done by an internal web server, at the URL http://127.0.0.1:8888.

Impress your friends with this musical magic trick!

With a Virtual Synth       |With Keyboard in Daw Mode  | With Rack Synth Device
:-------------------------:|:-------------------------:|:-------------------------:
<img src="media/ILC.png"  width="280"> | <img src="media/ILC3.png"  width="130"> | <img src="media/ILC2.png"  width="220">

# Recommanded usage:

```bash
pip install poetry
cd src
poetry install
poetry run python i-like-chopin.py
```

# Programs and libraries used:

* Python 3.10.12
* mido==1.2.10
* python-rtmidi==1.4.7
* PySide6==6.7.1
* netifaces2==0.0.22

# Soundfont

Soundfont used : https://musical-artifacts.com/artifacts/4161

Some other SoundFonts : https://sites.google.com/site/soundfonts4u/

# Thanks

Thank you to [cyri11e](https://github.com/cyri11e) for carrying out the program tests on MacOS and for his great patience.
