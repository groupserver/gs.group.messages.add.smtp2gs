# -*- coding: utf-8 -*-
'''Error values for a script. Taken from ``/usr/include/sysexits.h``
Copyright (c) 1987, 1993 The Regents of the University of California.
All rights reserved.
'''
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
from __future__ import unicode_literals
#: Successful termination
EX_OK = 0

#: The command was used incorrectly, e.g., with the wrong number of arguments,
#: a bad flag, a bad syntax in a parameter, or whatever.
EX_USAGE = 64

#: The input data was incorrect in some way.This should only be used for
#: user's data & not system files
EX_DATAERR = 65

#: The user specified did not exist. This might be used for mail addresses or
#: remote logins.
EX_NOUSER = 67

#: The remote system returned something that was "not possible" during a
#: protocol exchange.
EX_PROTOCOL = 76

#:temporary failure, indicating something that is not really an error. In
#: sendmail, this means that a mailer (e.g.) could not create a connection,
#: and the request should be reattempted later.
EX_TEMPFAIL = 75

#: Configuration error
EX_CONFIG = 78


#: A dictionary of issues mapped to standard error values.
exit_vals = {
    'success': EX_OK,
    'input_file_empty': EX_DATAERR,
    'input_file_too_large': EX_DATAERR,
    'config_error': EX_CONFIG,
    'url_bung': EX_USAGE,
    'communication_failure': EX_PROTOCOL,
    'socket_error': EX_PROTOCOL,
    'locked': EX_TEMPFAIL,  # Postfix will try again later
    'no_x_original_to': EX_DATAERR,
    'json_decode_error': EX_PROTOCOL,
    'no_group': EX_NOUSER, }
