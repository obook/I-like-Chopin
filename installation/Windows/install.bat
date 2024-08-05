@echo off
:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
:: Execute stuff...
python.exe -m pip install --upgrade pip
python.exe -m pip install poetry
echo Excecute in src folder : poetry run python i-like-chopin.py
:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Vous devez installer Python3 depuis https://www.python.org/ pour utiliser ce programme
set /p DUMMY=Appuyer sur entrer pour quitter...
:eof
