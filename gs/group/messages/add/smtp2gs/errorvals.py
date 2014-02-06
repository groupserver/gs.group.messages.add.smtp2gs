# -*- coding: utf-8 -*-
# See /usr/include/sysexits.h
# Copyright (c) 1987, 1993
#      The Regents of the University of California.  All rights reserved.
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
EX_OK = 0
EX_USAGE = 64
EX_DATAERR = 65
EX_NOUSER = 67
EX_PROTOCOL = 76
EX_TEMPFAIL = 75
EX_CONFIG = 78
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
