'''
!!! NOT USED FOR INSTANCE
'''
import sys
from cx_Freeze import setup, Executable

# Les dépendances sont automatiquement détectées, mais il peut être nécessaire de les ajuster.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6", "python-rtmidi"],
}

# base="Win32GUI" devrait être utilisé uniquement avec l’app Windows GUI 
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="I-Love-Chopin",
    version="1.0.0",
    description="Funny Midi Player",
    options={"build_exe": build_exe_options},
    executables=[Executable("i-like-chopin.py", base=base)],
)
