# -*- coding: utf-8 -*-
'''The core code for the ``smtp2gs`` script.'''
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
# Standard modules
import atexit
from email import message_from_string
from socket import gaierror
import sys
if (sys.version_info < (3, )):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse  # lint:ok
# GroupServer modules
from gs.config import Config, ConfigError
# Local modules
from .errorvals import exit_vals
from .getargs import get_args
from .locker import get_lock
from .servercomms import (get_group_info_from_address, NotOk, add_post,
                          relay_email)
from .xverp import is_an_xverp_bounce, handle_bounce

#: ``True`` if the current process is responsible for locking.
weLocked = False

#: The global lock object. See :func:`.locker.get_lock`.
lock = None

# The error-messages that are written to STDERR conform to RFC 3463
# <http://tools.ietf.org/html/rfc3463>. If a problem can be changed with an
# alteration to the configuration then a 4.x.x error will be returned.


def add_post_to_groupserver(progName, url, listId, emailMessage, token,
                            relayAddressPrefix):
    '''Add a post to a GroupServer group.

:param str progName: The name of the current program (for error messages)
:param str url: The URL for the host to connect to.
:param str listId: The identifier for the list (group) to add the group to.
                   If set to None or '' then the ``x-original-to`` header
                   will be examined to determine the email address which is
                   used to look up the ID of the group.
:param str emailMessage: The entire email message to add (including the
                         header)
:param str token: The authentiation token to pass to GroupServer.
:return: Nothing. :func:`sys.exit` may be called to terminate the program if
                  there is a problem, returning a value from
                  :mod:`.errorvals`.

The :func:`add_post_to_groupserver` function is the core of the ``smtp2gs``
script. It checks that the email is valid (using the :mod:`email` module),
ensures it is not a bounce (:mod:`.xverp`), gathers information about the
group, and finally adds the post (:mod:`.servercomms`).
'''
    # WARNING: multiple exit points below thanks to "sys.exit" calls.
    # Dijkstra will hate me for this.

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
    netloc = parsedUrl.netloc  # Has a port in it
    usessl = parsedUrl.scheme == 'https'

    email = message_from_string(emailMessage)

    to = email['To']
    if (to.startswith(relayAddressPrefix)):
        relay_email(netloc, usessl, emailMessage, token)
        sys.exit(exit_vals['success'])

    xOriginalTo = email['x-original-to']
    if ((xOriginalTo is None) and (not listId)):
        m = '5.1.3 No "x-original-to" header in the email message.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['no_x_original_to'])

    if is_an_xverp_bounce(xOriginalTo):
        handle_bounce(netloc, usessl, xOriginalTo, token)
        m = '2.1.5 The XVERP bounce was processed.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['success'])
    elif listId:  # We were explicitly passed the group id
        groupToSendTo = listId
    else:  # Get the information about the group
        groupInfo = get_group_info_from_address(netloc, usessl,
                                                xOriginalTo, token)
        groupToSendTo = groupInfo['groupId']

    if not(groupToSendTo):
        m = '5.1.1 There is no such group on this site.'
        sys.stderr.write(m)
        sys.exit(exit_vals['no_group'])

    # Finally, add the email to the group.
    add_post(netloc, usessl, groupToSendTo, emailMessage, token)


@atexit.register
def cleanup_lock():
    '''Unlock the file lock.

The :func:`cleanup_lock` method is decorated with :func:`atexit.register` so
it is always called. However, it only unlocks the lock if (and only if) it
is the process responsible for locking the lock.
'''
    global weLocked, lock
    if weLocked:
        ## VVVVVVVVVVVVVVVVVVVVVVVVVVV ##
        ## vvvvvvvvvvvvvvvvvvvvvvvvvvv ##
        lock.release()  # Very important!
        ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
        ## AAAAAAAAAAAAAAAAAAAAAAAAAAA ##


def MiB_to_B(mb):
    '''Pretty-print a file size, in Megabytes (2**20)
'''
    retval = mb * (2 ** 20)
    assert retval > mb
    return retval


def get_token_from_config(configSet, configFileName):
    '''Get the authentication token from the config.

:param str configSet: The name of the configuration set to look up (see
                      :class:`gs.config.Config`)
:param str configFileName: The name of the configuration file that contains
                           the token.
:return: The authentication token for ``configSet`` in ``configFileName``
:rtype: ``str``
:raises ValueError: The token was not present in ``configSet``.
'''
    config = Config(configSet, configFileName)
    config.set_schema('webservice', {'token': str})
    ws = config.get('webservice')
    retval = ws['token']
    if not retval:
        m = 'The token was not set.'
        raise ValueError(m)
    return retval


def get_relay_address_prefix_from_config(configSet, configFileName):
    '''Get the prefix used to mark email addresses to relay from the config.

:param str configSet: The name of the configuration set to look up (see
                      :class:`gs.config.Config`)
:param str configFileName: The name of the configuration file that contains
                           the token.
:return: The address prefix for ``configSet`` in ``configFileName``, or 'p-'
         if absent.
:rtype: ``str``
'''
    config = Config(configSet, configFileName)
    config.set_schema('smtp', {'relay-address-prefix': str})
    ws = config.get('smtp')
    retval = ws['relay-address-prefix']
    if not retval:
        retval = 'p-'
    return retval


def main(configFileName='etc/gsconfig.ini'):
    '''The main function in the ``smtp2gs`` script

:param str configFileName: The name of the configuration file for
                           GroupServer.
:return: Nothing. :func:`sys.exit` is called with one of the values from
                  :mod:`.errorvals`.

The :func:`main` function parses the command-line arguments, retrieves the
authentication token, opens the email message, and then calls
:func:`add_post_to_groupserver`.
'''
    args = get_args(configFileName)
    try:
        token = get_token_from_config(args.instance, args.config)
    except ConfigError as ce:
        m = '4.3.5: Error with the configuration file "%s":\n%s\n' %\
            (args.config, ce.message)
        sys.stderr.write(m)
        sys.exit(exit_vals['config_error'])

    relayAddressPrefix = get_relay_address_prefix_from_config(
        args.instance, args.config)

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
                                emailMessage, token, relayAddressPrefix)
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
