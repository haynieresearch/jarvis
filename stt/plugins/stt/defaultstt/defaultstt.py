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
import requests
from core import plugin

class WitAiSTTPlugin(plugin.STTPlugin):
    def __init__(self, *args, **kwargs):
        plugin.STTPlugin.__init__(self, *args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.key = self.profile['keys']['witai']


    def transcribe(self, fp):
        sttHeaders = {'Authorization': 'Bearer %s' % self.key,
                      'accept': 'application/json',
                      'Content-Type': 'audio/wav'}

        audio = fp.read()
        sttData = requests.post('https://api.wit.ai/speech?v=20170307',
                          data=audio,
                          headers=sttHeaders)

        try:
            sttData.raise_for_status()
        except requests.exceptions.HTTPError:
            self._logger.critical('Request failed with http status %d',
                                  sttData.status_code)
            return []
            if sttData.status_code == requests.codes['forbidden']:
                self._logger.warning('Request forbidden, check your API key')
            return []

        try:
            sttResponse = sttData.json()['_text']
            if len(sttResponse) == 0:
                raise ValueError('Nothing transcribed.')
        except ValueError as e:
            self._logger.warning('Empty response: %s', e.args[0])
            results = []
        except (KeyError, IndexError):
            self._logger.warning('Cannot parse response.', exc_info=True)
            results = []
        else:
            results = [sttResponse.upper()]
            self._logger.info('Transcribed: %r', results)
        return results
