# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from __future__ import absolute_import, unicode_literals
# Standard modules
import atexit
from email import message_from_string
from socket import gaierror
import sys
from urlparse import urlparse
# GroupServer modules
from gs.config.config import Config, ConfigError
# Local modules
from .errorvals import exit_vals
from .getargs import get_args
from .locker import get_lock
from .servercomms import get_group_info_from_address, NotOk, add_post
from .xverp import is_an_xverp_bounce, handle_bounce

weLocked = False
lock = None

# The error-messages that are written to STDERR conform to RFC 3463
# <http://tools.ietf.org/html/rfc3463>. If a problem can be changed with an
# alteration to the configuration then a 4.x.x error will be returned.


def add_post_to_groupserver(progName, url, listId, emailMessage, token):
    # WARNING: multiple exit points below thanks to "sys.exit" calls. Dijkstra
    # will hate me for this.

    # First, get the lock or die!!
    global weLocked, lock
    lock = get_lock()
    if not lock.i_am_locking():
        m = '4.4.5 Not processing the message, as the system is too busy.'
        sys.stderr.write(m)
        sys.exit(exit_vals['locked'])
    weLocked = True

    parsedUrl = urlparse(url)
    if not parsedUrl.hostname:
        m = '4.5.2 No host in the URL <%s>\n' % (url)
        sys.stderr.write(m)
        sys.exit(exit_vals['url_bung'])
    hostname = parsedUrl.netloc
    usessl = parsedUrl.scheme == 'https'

    email = message_from_string(emailMessage)
    xOriginalTo = email['x-original-to']
    if xOriginalTo is None:
        m = '5.1.3 No "x-original-to" header in the email message.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['no_x_original_to'])

    if is_an_xverp_bounce(xOriginalTo):
        handle_bounce(hostname, xOriginalTo, token)
        m = '2.1.5 The XVERP bounce was processed.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['success'])
    elif listId:  # We were explicitly passed the group id
        groupToSendTo = listId
    else:  # Get the information about the group
        groupInfo = get_group_info_from_address(hostname, xOriginalTo, token,
                                                usessl)
        groupToSendTo = groupInfo['groupId']

    if not(groupToSendTo):
        m = '5.1.1 There is no such group on this site.'
        sys.stderr.write(m)
        sys.exit(exit_vals['no_group'])

    # Finally, add the email to the group.
    add_post(hostname, groupToSendTo, emailMessage, token, usessl)


@atexit.register
def cleanup_lock():
    global weLocked, lock
    if weLocked:
        ## VVVVVVVVVVVVVVVVVVVVVVVVVVV ##
        ## vvvvvvvvvvvvvvvvvvvvvvvvvvv ##
        lock.release()  # Very important!
        ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
        ## AAAAAAAAAAAAAAAAAAAAAAAAAAA ##


def MiB_to_B(mb):
    retval = mb * (2 ** 20)
    assert retval > mb
    return retval


def get_token_from_config(configSet, configFileName):
    config = Config(configSet, configFileName)
    config.set_schema('webservice', {'token': str})
    ws = config.get('webservice')
    retval = ws['token']
    if not retval:
        m = 'The token was not set.'
        raise ValueError(m)
    return retval


def main(configFileName='etc/gsconfig.ini'):
    args = get_args(configFileName)
    try:
        token = get_token_from_config(args.instance, args.config)
    except ConfigError as ce:
        m = '4.3.5: Error with the configuration file "%s":\n%s\n' %\
            (args.config, ce.message)
        sys.stderr.write(m)
        sys.exit(exit_vals['config_error'])

    emailMessage = args.file.read()
    args.file.close()
    l = len(emailMessage)
    if l == 0:
        m = '5.3.0 The file containing the email was empty.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_empty'])
    elif (MiB_to_B(args.maxSize) < l):
        m = '5.3.4 Email message too large (%d bytes, rather than %d '\
            'bytes).\n' % (len(emailMessage), MiB_to_B(args.maxSize))
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_too_large'])

    try:
        add_post_to_groupserver(sys.argv[0], args.url, args.listId,
                                emailMessage, token)
    except gaierror as g:
        m = '4.4.4 Error connecting to the server while processing '\
            'the message:\n%s\n' % (g)
        sys.stderr.write(m)
        sys.exit(exit_vals['socket_error'])
    except NotOk as ne:
        m = '4.5.0 Error communicating with the server while '\
            'processing the message:\n%s\n' % (ne)
        sys.stderr.write(m)
        sys.exit(exit_vals['communication_failure'])
    except ValueError:
        m = '4.5.0 Could not decode the data returned by the server '\
            'while processing the\nmessage. Check the token?\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['json_decode_error'])
    else:
        sys.exit(exit_vals['success'])

if __name__ == '__main__':
    main()
