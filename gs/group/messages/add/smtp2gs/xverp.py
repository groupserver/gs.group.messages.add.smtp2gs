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
import re
from .servercomms import add_bounce

# XVERP addresses look like listId+userMailbox=user.domain@this.server
XVERP_RE = re.compile('(.*?)\+(.*?)\=(.*?)\@(.*)')


def is_an_xverp_bounce(toAddress):
    result = XVERP_RE.search(toAddress)
    retval = bool(result) and (len(result.groups()) == 4)
    assert type(retval) == bool
    return retval


def handle_bounce(hostname, toAddress, token, usessl):
    groups = XVERP_RE.search(toAddress).groups()
    listAddress = '@'.join((groups[0], groups[3]))  # listId@this.server
    userAddress = '@'.join((groups[1], groups[2]))  # userMailbox@user.domain
    add_bounce(hostname, userAddress, listAddress, token, usessl)
