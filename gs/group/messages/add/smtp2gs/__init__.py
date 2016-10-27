# -*- coding: utf-8 -*-
'''The script for adding an email (from SMTP) to GroupServer'''
from enum import Enum


class TimeSource(Enum):
    '''Where to get the time-stamp of the post'''
    message = 1  #: Get the time stamp from the :mailheader:`Date` header
    server = 2  #: Get the time stamp from the clock on the server
