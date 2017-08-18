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

import gettext

TEST_PROFILE = {
    'prefers_email': False,
    'timezone': 'US/Eastern',
    'phone_number': '012344321',
    'weather': {
        'location': 'New York',
        'unit': 'Fahrenheit'
    }
}


class TestMic(object):
    def __init__(self, inputs=[]):
        self.inputs = inputs
        self.idx = 0
        self.outputs = []

    def wait_for_keyword(self, keyword="JARVIS"):
        return

    def active_listen(self, timeout=3):
        if self.idx < len(self.inputs):
            self.idx += 1
            return [self.inputs[self.idx - 1]]
        return [""]

    def say(self, phrase):
        self.outputs.append(phrase)


def get_plugin_instance(plugin_class, *extra_args):
    info = type('', (object,), {
        'name': 'pluginunittest',
        'translations': {
            'en-US': gettext.NullTranslations()
            }
        })()
    args = tuple(extra_args) + (info, TEST_PROFILE)
    return plugin_class(*args)
