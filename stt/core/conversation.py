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
from . import i18n
#  from notifier import Notifier


class Conversation(i18n.GettextMixin):
    def __init__(self, mic, brain, profile):
        translations = i18n.parse_translations(paths.data('locale'))
        i18n.GettextMixin.__init__(self, translations, profile)
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.profile = profile
        self.brain = brain
        self.translations = {

        }
        #  self.notifier = Notifier(profile)

    def greet(self):
        salutation = self.gettext("Jarvis speech to text engine is online.")
        #self.mic.say(salutation)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.debug('Starting to handle conversation.')
        while True:
            # Print notifications until empty
            """notifications = self.notifier.get_all_notifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))"""

            input = self.mic.listen()

            if input:
                plugin, text = self.brain.query(input)
                if plugin and text:
                    try:
                        plugin.handle(text, self.mic)
                    except Exception:
                        self._logger.error('Failed to execute module',
                                           exc_info=True)
                        self.mic.say(self.gettext(
                            "I'm sorry. I had some trouble with that " +
                            "operation. Please try again later."))
                    else:
                        self._logger.debug("Handling of phrase '%s' by " +
                                           "module '%s' completed", text,
                                           plugin.info.name)
            else:
                self.mic.say(self.gettext("Pardon?"))
