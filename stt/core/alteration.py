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

import re


def detect_years(input):
    YEAR_REGEX = re.compile(r'(\b)(\d\d)([1-9]\d)(\b)')
    return YEAR_REGEX.sub('\g<1>\g<2> \g<3>\g<4>', input)


def clean(input):
    """
        Manually adjust output text before it's translated into
        actual speech by the TTS system. This is to fix minior
        idiomatic issues, for example, that 1901 is pronounced
        "one thousand, ninehundred and one" rather than
        "nineteen oh one".

        Arguments:
        input -- original speech text to-be modified
    """
    return detect_years(input)
