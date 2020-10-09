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

import sys
import logging
import argparse

from .application import application
from application import USE_STANDARD_MIC, USE_TEXT_MIC, USE_BATCH_MIC


def main(args=None):
    parser = argparse.ArgumentParser(description='Jarvis Voice Control Center')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug messages')
    list_info = parser.add_mutually_exclusive_group(required=False)
    list_info.add_argument('--list-plugins', action='store_true',
                           help='List plugins and exit')
    list_info.add_argument('--list-audio-devices', action='store_true',
                           help='List audio devices and exit')
    mic_mode = parser.add_mutually_exclusive_group(required=False)
    mic_mode.add_argument('--local', action='store_true',
                          help='Use text input instead of a real microphone')
    mic_mode.add_argument('--batch', dest='batch_file', metavar="FILE",
                          type=argparse.FileType('r'),
                          help='Batch mode using a text file with text' +
                          'commands audio filenames at each line.')
    p_args = parser.parse_args(args)

    print("\nJarvis Speech to Text Engine")
    print("Haynie Research & Development LLC\n")

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if p_args.debug else logging.INFO)
#    logging.basicConfig(level=logging.DEBUG)
    # Select Mic
    if p_args.local:
        # Use Local text mic
        used_mic = USE_TEXT_MIC
    elif p_args.batch_file is not None:
        # Use batched mode mic, pass a file too
        used_mic = USE_BATCH_MIC
    else:
        used_mic = USE_STANDARD_MIC

    app = application.core(use_mic=used_mic,
                             batch_file=p_args.batch_file)
    if p_args.list_plugins:
        app.list_plugins()
        sys.exit(1)
    elif p_args.list_audio_devices:
        app.list_audio_devices()
        sys.exit(0)
    app.run()


if __name__ == '__main__':
    main()
