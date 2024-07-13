#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 11:34:35 2024
@author: obooklage
"""

import multiprocessing
import time

def your_proc_function():
    while True:
        print("Hello")
        time.sleep(1)

proc = multiprocessing.Process(target=your_proc_function, args=())
proc.start()
time.sleep(5)
# Terminate the process
proc.terminate()  # sends a SIGTERM
