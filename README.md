# I like Chopin
Funny program for play like Chopin.
(tribute to Gazebo)

<p align="center">
    <img src="media/20240717_192901.png"  width="600">
</p>

"I like Chopin" is a very special MIDI player for Linux, Mac or Windows that uses Python 3, the Mido library and Qt6. Any random key pressed on a physical master keyboard plays the correct note from the MIDI file. When all keys are released, the MIDI player stops. You need a physical MIDI master keyboard connected to the computer and a virtual synthesizer.

Impress your friends with this musical magic trick!

With Rack Synth Device     |  With Virtual Synth
:-------------------------:|:-------------------------:
<img src="media/ILC2.png"  width="280"> |  <img src="media/ILC.png"  width="280">

Requirements:

* Python 3.1x
* mido==1.2.10
* python-rtmidi==1.4.7
* PySide6==6.7.1
