@echo off
python --version 3>NUL
if errorlevel 1 goto errorNoPython
cd src
poetry run python i-like-chopin.py
goto:eof
:errorNoPython
echo.
echo Error^: Install python3 from https://www.python.org/
set /p DUMMY=Press any key...
:eof
