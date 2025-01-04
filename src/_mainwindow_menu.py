#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:23:12 2024
@author: obooklage
"""


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

    def TriggeredActionQuit(self):
        self.Quit()

    def TriggeredFavorite(self, action):
        self.MidifileChange(action.data())
