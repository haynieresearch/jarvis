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

class MicrosoftSttPlugin(plugin.STTPlugin):
    def __init__(self, *args, **kwargs):
        plugin.STTPlugin.__init__(self, *args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.key = self.profile['keys']['bing_speech']

    def transcribe(self, fp):
        tokenHeaders = {'Ocp-Apim-Subscription-Key': '%s' % self.key,
                        'Content-type': 'application/x-www-form-urlencoded',
                        'Content-Length': '0'}

        keyData = requests.post('https://api.cognitive.microsoft.com/sts/v1.0/issueToken',
                          headers=tokenHeaders)

        token = keyData.content

        sttHeaders = {'Authorization': 'Bearer %s' % token,
                         'Content-Type': 'audio/wav; codec="audio/pcm"; samplerate=16000'}

        audio = fp.read()

        sttData = requests.post('https://speech.platform.bing.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US',
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
            sttStatus = sttData.json()['RecognitionStatus']
            if sttStatus == 'InitialSilenceTimeout':
                raise ValueError('Audio was empty.')
            elif sttStatus == 'NoMatch':
                raise ValueError('Unable to transcribe transmitted audio.')
            elif sttStatus != 'Success':
                raise ValueError('Unable to transcribe speech.')

            sttResponse = sttData.json()['DisplayText']
            if len(sttResponse) == 0:
                raise ValueError('Nothing to transcribed.')
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
