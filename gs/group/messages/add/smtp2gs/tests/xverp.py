# -*- coding: utf-8 -*-
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
from unittest import TestCase
from mock import MagicMock
from gs.group.messages.add.smtp2gs.xverp import (is_an_xverp_bounce,
                                                 handle_bounce)
import gs.group.messages.add.smtp2gs.xverp as smtp2gs_xverp


class TestXVERP(TestCase):
    'Tests for XVERP handling'
    xverpAddr = 'development+mpj17=onlinegroups.net@groupserver.org'

    def test_is_xverp(self):
        'Test that an XVERP address is seen as an XVERP address'
        r = is_an_xverp_bounce(self.xverpAddr)
        self.assertTrue(r)

    def test_isnt_xverp(self):
        '''Test that an ordinary address is seen as an ordinary address,
        rather than an XVERP address'''
        addr = 'development@groupsverver.org'
        r = is_an_xverp_bounce(addr)
        self.assertFalse(r)

    def test_none(self):
        r = is_an_xverp_bounce(None)
        self.assertFalse(r)

    def test_blank(self):
        r = is_an_xverp_bounce(b'')
        self.assertFalse(r)

    def test_handle_bounce(self):
        'Test the call to handle_bounce'
        smtp2gs_xverp.add_bounce = MagicMock()
        handle_bounce('gstest', True, self.xverpAddr, 'token')
        self.assertEqual(1, smtp2gs_xverp.add_bounce.call_count)
        args, kw_args = smtp2gs_xverp.add_bounce.call_args
        self.assertEqual('gstest', args[0])
        self.assertTrue(args[1])
        self.assertEqual('mpj17@onlinegroups.net', args[2])
        self.assertEqual('development@groupserver.org', args[3])
        self.assertEqual('token', args[4])
