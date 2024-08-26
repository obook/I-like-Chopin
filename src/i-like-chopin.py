#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

# Please read README.md, section "Recommanded usage"

from mainwindow import start


while True:
    try:
        start()
        break
    except Exception as e:
        print(f"Program errored out! [{e}]")
        print("Retrying ... ")
