#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:23:12 2024
@author: obooklage
"""
# from PySide6.QtGui import QAction

import os
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

class menu:

    def _SetMenu(self):

        action_quit = self.ui.actionQuit
        action_quit.triggered.connect(self.TriggeredActionQuit)

        action_favorites = self.ui.menuFavorites
        file_dic = self.Playlist.GetPlayList()
        for dict in file_dic:
            title = dict['title']
            action = action_favorites.addAction(title)
            action.setData(dict['path'])
        action_favorites.triggered.connect(self.TriggeredFavorite)

        '''
        # Systray
        ICON_SYSTRAY = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "icons", "svg", "i-like-chopin.svg"
        )

        icon = QIcon(ICON_SYSTRAY)

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)



        # Create the menu
        menu = QMenu()
        action = QAction("Open Main Window")
        menu.addAction(action)

        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(self.TriggeredActionQuit())
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)
        tray.setToolTip("I like Chopin")
        '''

    def TriggeredActionQuit(self):
        self.Quit()

    def TriggeredFavorite(self, action):
        self.MidifileChange(action.data())
