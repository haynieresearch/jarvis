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

import os.path
import logging


def parse_batch_file(fp):
    # parse given batch file and get the filenames or commands
    for line in fp:
        line = line.partition('#')[0].rstrip()
        if line:
            yield line


class Mic(object):
    def __init__(self, passive_stt_engine, active_stt_engine,
                 batch_file, keyword='JARVIS'):
        self._logger = logging.getLogger(__name__)
        self._keyword = keyword
        self.passive_stt_engine = passive_stt_engine
        self.active_stt_engine = active_stt_engine
        self._commands = parse_batch_file(batch_file)

    def transcribe_command(self, command):
        # check if command is a filename
        if os.path.isfile(command):
            # handle it as mic input
            try:
                fp = open(command, 'r')
            except (OSError, IOError) as e:
                self._logger.error('Failed to open "%s": %s',
                                   command, e.strerror)
            else:
                transcribed = self.active_stt_engine.transcribe(fp)
                fp.close()
        else:
            # handle it as text input
            transcribed = [command]
        return transcribed

    def wait_for_keyword(self, keyword="JARVIS"):
        return

    def active_listen(self, timeout=3):
        try:
            command = next(self._commands)
        except StopIteration:
            raise SystemExit
        else:
            transcribed = self.transcribe_command(command)
            if transcribed:
                print('YOU: %r' % transcribed)
            return transcribed

    def listen(self):
        return self.active_listen()

    def say(self, phrase, OPTIONS=None):
        print("JARVIS: %s" % phrase)
