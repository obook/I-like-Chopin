:: Author : obooklage
:: Date : 28/01/2025
:: Desc1 : Update midi library and i-love-chopin
:: Desc2 : Launch i-love-chopin and brave web browser
::
:: Install poetry under Windows in PowerShell with the official installer (tested) :
:: https://python-poetry.org/docs/#installing-with-the-official-installer
::
:: Install git for Linux :
:: https://git-scm.com/downloads/win
::

@echoff

set applicationpath=%HOMEDRIVE%%HOMEPATH%\Documents\GitHub\I-like-Chopin
set midipath=%HOMEDRIVE%%HOMEPATH%\Music\midi

:: update application
echo Update %applicationpath%
cd %applicationpath%
git pull

:: update midilib
echo Update %midipath%
cd %midipath%
git pull

:: Launch i-love-chopin
cd %applicationpath%\src
poetry run python i-like-chopin.py &

::cd %HOMEDRIVE%%HOMEPATH%\Desktop

