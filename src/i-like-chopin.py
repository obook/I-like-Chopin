#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import sys
from mainwindow import start

def is_module_available(module_name, quit=True, default=None):
    """Tool for check dependances"""
    if sys.version_info < (3, 0):
        # python 2
        import importlib
        done = importlib.find_loader(module_name)
    elif sys.version_info <= (3, 3):
        # python 3.0 to 3.3
        import pkgutil
        done = pkgutil.find_loader(module_name)
    elif sys.version_info >= (3, 4):
        # python 3.4 and above
        import importlib
        done = importlib.util.find_spec(module_name)
    if not done and quit:
        if default:
            module_name = default
        print(f"LIBRARY ERROR : Missing module '{module_name}'. Use for example : pip install {module_name}")
        sys.exit(-1)
    return done

# Check modules
is_module_available('PySide6')
is_module_available('mido')
if not is_module_available('python-rtmidi', False):
    is_module_available('rtmidi', True, 'python-rtmidi')

start()
