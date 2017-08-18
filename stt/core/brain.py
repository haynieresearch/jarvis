# -*- coding: utf-8 -*-
#**********************************************************
#* CATEGORY    JARVIS HOME AUTOMTION
#* GROUP       SPEECH TO TEXT
#* AUTHOR      LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#**********************************************************
#Jarvis Home Automation
#Copyright (C) 2017  Haynie Research & Development

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging
from . import paths


class Brain(object):
    def __init__(self, config):
        self._plugins = []
        self._logger = logging.getLogger(__name__)
        self._config = config

    def add_plugin(self, plugin):
        self._plugins.append(plugin)
        self._plugins = sorted(
            self._plugins, key=lambda p: p.get_priority(), reverse=True)

    def get_plugins(self):
        return self._plugins

    def get_standard_phrases(self):
        try:
            language = self._config['language']
        except KeyError:
            language = None
        if not language:
            language = 'en-US'

        phrases = []

        with open(paths.data('standard_phrases', "%s.txt" % language),
                  mode="r") as f:
            for line in f:
                phrase = line.strip()
                if phrase:
                    phrases.append(phrase)

        return phrases

    def get_plugin_phrases(self):
        """
        Gets phrases from all plugins.

        Returns:
            A list of phrases from all plugins.
        """
        phrases = []

        for plugin in self._plugins:
            phrases.extend(plugin.get_phrases())

        return sorted(list(set(phrases)))

    def get_all_phrases(self):
        """
        Gets a combined list consisting of standard phrases and plugin phrases.

        Returns:
            A list of phrases.
        """
        return self.get_standard_phrases() + self.get_plugin_phrases()

    def query(self, texts):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module

        Returns:
            A tuple containing a text and the module that can handle it
        """
        for plugin in self._plugins:
            for text in texts:
                if plugin.is_valid(text):
                    self._logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, plugin.info.name)
                    return (plugin, text)
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)
        return (None, None)
