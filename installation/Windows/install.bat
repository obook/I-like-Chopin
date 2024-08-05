@echo off
:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
:: Execute stuff...
python.exe -m pip install --upgrade pip
python.exe -m pip install poetry
echo Execute in src folder : poetry run python i-like-chopin.py
:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Install Python3 from https://www.python.org/ pour utiliser ce programme
set /p DUMMY=Press any key...
:eof
