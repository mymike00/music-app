# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2013 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

"""Music app autopilot tests."""

from __future__ import absolute_import

from autopilot.matchers import Eventually
from testtools.matchers import Equals, LessThan

from music_app.tests import MusicTestCase


class TestMainWindow(MusicTestCase):

    def setUp(self):
        super(TestMainWindow, self).setUp()
        self.assertThat(
            self.main_view.visible, Eventually(Equals(True)))
        #wait for activity indicator to stop spinning
        spinner = lambda: self.main_view.get_spinner().running
        self.assertThat(spinner, Eventually(Equals(False)))

    def test_reads_music_library(self):
        """ tests if the music library is populated from our
        fake mediascanner database"""

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        title = lambda: self.main_view.currentTracktitle
        artist = lambda: self.main_view.currentArtist
        self.assertThat(title,
                        Eventually(Equals("Foss Yeaaaah! (Radio Edit)")))
        self.assertThat(artist, Eventually(Equals("Benjamin Kerensa")))

    def test_play_pause_library(self):
        """ Test playing and pausing a track (Music Library must exist) """

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        # click back button
        back_button = self.main_view.get_back_button()
        self.pointing_device.click_object(back_button)

        self.main_view.show_toolbar()
        playbutton = self.main_view.get_play_button()

        """ Track is playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))
        self.pointing_device.click_object(playbutton)

        """ Track is not playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(False)))

        """ Track is playing"""
        self.pointing_device.click_object(playbutton)
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))

    def test_play_pause_now_playing(self):
        """ Test playing and pausing a track (Music Library must exist) """

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        playbutton = self.main_view.get_now_playing_play_button()

        """ Track is playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))
        self.pointing_device.click_object(playbutton)

        """ Track is not playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(False)))

        """ Track is playing"""
        self.pointing_device.click_object(playbutton)
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))

    def test_next(self):
        """ Test going to next track (Music Library must exist) """

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        forwardbutton = self.main_view.get_forward_button()

        title = lambda: self.main_view.currentTracktitle
        artist = lambda: self.main_view.currentArtist
        self.assertThat(title,
                        Eventually(Equals("Foss Yeaaaah! (Radio Edit)")))
        self.assertThat(artist, Eventually(Equals("Benjamin Kerensa")))

        """ Track is playing"""
        self.assertThat(self.main_view.isPlaying, Equals(True))
        self.pointing_device.click_object(forwardbutton)

        """ Track is playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))
        self.assertThat(title, Eventually(Equals("Swansong")))
        self.assertThat(artist, Eventually(Equals("Josh Woodward")))

    def test_previous_and_mp3(self):
        """ Test going to previous track, last item must be an MP3
            (Music Library must exist) """

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        repeatbutton = self.main_view.get_repeat_button()

        previousbutton = self.main_view.get_previous_button()

        title = lambda: self.main_view.currentTracktitle
        artist = lambda: self.main_view.currentArtist
        self.assertThat(title,
                        Eventually(Equals("Foss Yeaaaah! (Radio Edit)")))
        self.assertThat(artist, Eventually(Equals("Benjamin Kerensa")))

        """ Track is playing, repeat is off"""
        self.assertThat(self.main_view.isPlaying, Equals(True))
        self.pointing_device.click_object(repeatbutton)
        self.pointing_device.click_object(previousbutton)

        """ Track is playing"""
        self.assertThat(self.main_view.isPlaying, Eventually(Equals(True)))
        self.assertThat(title, Eventually(Equals("TestMP3Title")))
        self.assertThat(artist, Eventually(Equals("TestMP3Artist")))

    def test_shuffle(self):
        """ Test shuffle (Music Library must exist) """

        # populate queue
        first_genre_item = self.main_view.get_first_genre_item()
        self.pointing_device.click_object(first_genre_item)

        shufflebutton = self.main_view.get_shuffle_button()

        forwardbutton = self.main_view.get_forward_button()

        previousbutton = self.main_view.get_previous_button()

        title = lambda: self.main_view.currentTracktitle
        artist = lambda: self.main_view.currentArtist
        self.assertThat(title,
                        Eventually(Equals("Foss Yeaaaah! (Radio Edit)")))
        self.assertThat(artist, Eventually(Equals("Benjamin Kerensa")))

        """ Track is playing, shuffle is turned on"""
        self.assertThat(self.main_view.isPlaying, Equals(True))
        self.pointing_device.click_object(shufflebutton)
        self.assertThat(self.main_view.random, Eventually(Equals(True)))

        forward = True
        count = 0
        while True:
            self.assertThat(count, LessThan(100))

            if (!self.main_view.toolbarShown):
                self.main_view.show_toolbar()

            if forward:
                self.pointing_device.click_object(forwardbutton)
            else:
                self.pointing_device.click_object(previousbutton)

            """ Track is playing"""
            self.assertThat(self.main_view.isPlaying,
                            Eventually(Equals(True)))
            if (self.main_view.currentTracktitle == "TestMP3Title" and
                    self.main_view.currentArtist == "TestMP3Artist"):
                break
            else:
                forward = not forward
                count += 1
