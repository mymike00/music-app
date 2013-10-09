# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2013 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

"""Music app autopilot emulators."""
from ubuntuuitoolkit import emulators as toolkit_emulators
from autopilot.input import Mouse
from time import sleep


class MainView(toolkit_emulators.MainView):

    """An emulator class that makes it easy to interact with the
    music-app.
    """
    retry_delay = 0.2

    def get_qml_view(self):
        """Get the main QML view"""
        return self.select_single("QQuickView")

    def get_main_view(self):
        return self.select_single("MainView", objectName="music")

    def get_toolbar(self):
        return self.select_single("MusicToolbar",
                                  objectName="musicToolbarObject")

    def select_many_retry(self, object_type, **kwargs):
        """Returns the item that is searched for with app.select_many
        In case of no item was not found (not created yet) a second attempt is
        taken 1 second later"""
        items = self.select_many(object_type, **kwargs)
        tries = 10
        while len(items) < 1 and tries > 0:
            sleep(self.retry_delay)
            items = self.select_many(object_type, **kwargs)
            tries = tries - 1
        return items

    def select_single_retry(self, object_type, **kwargs):
        """Returns the item that is searched for with app.select_single
        In case of the item was not found (not created yet) a second attempt is
        taken 1 second later."""
        item = self.select_single(object_type, **kwargs)
        tries = 10
        while item is None and tries > 0:
            sleep(self.retry_delay)
            item = self.select_single(object_type, **kwargs)
            tries = tries - 1
        return item

    def tap_item(self, item):
        self.pointing_device.move_to_object(item)
        self.pointing_device.press()
        sleep(2)
        self.pointing_device.release()

    def show_toolbar(self):
        # Get the toolbar object and create a mouse
        toolbar = self.get_toolbar()
        mouse = Mouse.create()

        # Move to the toolbar and get the position
        mouse.move_to_object(toolbar)
        x1, y1 = mouse.position()

        y1 -= (toolbar.height / 2) + 1  # get position at top of toolbar

        mouse.drag(x1, y1, x1, y1 - toolbar.height)

    def get_play_button(self):
        return self.select_single("UbuntuShape", objectName="playshape")

    def get_forward_button(self):
        return self.select_single("UbuntuShape", objectName="forwardshape")

    def get_player_control_title(self):
        return self.select_single("Label", objectName="playercontroltitle")

    def get_spinner(self):
        return self.select_single("ActivityIndicator",
                                  objectName="LoadingSpinner")
