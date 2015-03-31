# -*- coding: utf-8 -*-
'''XVERP handling.'''
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
import re
from .servercomms import add_bounce

#: The regular expression for matching an XVERP address. They look like
#: listId+userMailbox=user.domain@this.server
XVERP_RE = re.compile('(.*?)\+(.*?)\=(.*?)\@(.*)')


def is_an_xverp_bounce(toAddress):
    '''Test if an address in an XVERP bounce.

:param str toAddress: The address to check.
:return: ``True`` if the address is an XVERP bounce.
:rtype: bool'''
    result = XVERP_RE.search(toAddress) if toAddress else None
    retval = bool(result) and (len(result.groups()) == 4)
    assert type(retval) == bool
    return retval


def handle_bounce(netloc, usessl, toAddress, token):
    '''Record that an XVERP bounce has occurred.

:param str netloc: The host-name of the GroupServer site (can have a
    ``:port``).
:param bool usessl: ``True`` if TLS should be used with communicating with
    GroupServer.
:param str toAddress: The address that is bouncing.
:param str token: The token used to authenticate with GroupServer.
:return: Nothing.

The ``toAddress`` is decomposed to the email address of the person whose
inbox is bouncing, and this addresses is used to record the bounce.
'''
    groups = XVERP_RE.search(toAddress).groups()
    # listId@this.server
    listAddress = '@'.join((groups[0], groups[3]))
    # userMailbox@user.domain
    userAddress = '@'.join((groups[1], groups[2]))
    add_bounce(netloc, usessl, userAddress, listAddress, token)
