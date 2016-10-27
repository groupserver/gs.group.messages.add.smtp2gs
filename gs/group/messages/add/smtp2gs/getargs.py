# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from argparse import ArgumentParser, FileType


def get_args(configFileName):
    '''Get the command-line arguments

:param str configFileName: The name of the GroupServer configuration file.
:return: An argument parser.
:rtype: class:`argparse.ArgumentParser`
'''
    p = ArgumentParser(
        description='Add an email message to GroupServer.',
        epilog='Usually %(prog)s is called by a SMTP server (such as'
               'Postfix) in order to add an email message to message to '
               'a GroupServer group.')
    p.add_argument('url', metavar='url',
                   help='The URL for the GroupServer site.')
    p.add_argument('-m', '--max-size', dest='maxSize', type=int,
                   default=200,
                   help='The maximum size of the post that will be '
                        'accepted, in mebibytes (default %(default)sMiB).')
    p.add_argument('-l', '--list', dest='listId', default=None,
                   help='The list to send the message to. By default it is '
                        'extracted from the x-original-to header.')
    p.add_argument('-f', '--file', dest='file', default='-',
                   type=FileType('r'),
                   help='The name of the file that contains the message. '
                        'If omitted (or "%(default)s") standard-input will '
                        'be read.')
    p.add_argument('-t', '--time-source', choices=['server', 'message'], dest='timeSource',
                   default='server',
                   help='Where to get the time that the message was written. Using "%(default)s"'
                        'avoids issues caused by the clocks of the group members being incorrect.')
    p.add_argument('-c', '--config', dest='config', default=configFileName,
                   type=str,
                   help='The name of the GroupServer configuration file '
                        '(default "%(default)s") that contains the token '
                        'that will be used to authenticate the script when '
                        'it tries to add the email to the site.')
    p.add_argument('-i', '--instance', dest='instance', default='default',
                   type=str,
                   help='The identifier of the GroupServer instance '
                        'configuration to use (default "%(default)s").')
    retval = p.parse_args()
    return retval
