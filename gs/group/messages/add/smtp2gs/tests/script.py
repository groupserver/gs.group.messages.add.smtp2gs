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
from unittest import TestCase
from mock import MagicMock
from gs.group.messages.add.smtp2gs.script import (get_token_from_config,
    cleanup_lock)
import gs.group.messages.add.smtp2gs.script as gsscript


class TestScript(TestCase):
    tokenValue = 'tokenValue'

    def setUp(self):
        gsscript.Config.__init__ = MagicMock(return_value=None)
        gsscript.Config.set_schema = MagicMock()
        gsscript.Config.get = MagicMock(return_value={'token': self.tokenValue})
        gsscript.sys.exit = MagicMock()

        gsscript.lock = MagicMock()
        self.oldWeLocked = gsscript.weLocked

    def tearDown(self):
        gsscript.weLocked = self.oldWeLocked

    def test_get_token_from_config(self):
        'Test that we get the token from the config'
        r = get_token_from_config('default', 'gsconfig.ini')
        self.assertEqual(self.tokenValue, r)
        self.assertEqual(1, gsscript.Config.__init__.call_count)
        self.assertEqual(1, gsscript.Config.set_schema.call_count)
        self.assertEqual(1, gsscript.Config.get.call_count)
        args, kw_args = gsscript.Config.__init__.call_args
        self.assertEqual('default', args[0])
        self.assertEqual('gsconfig.ini', args[1])

    def test_cleanup_lock_unlock(self):
        'Test that cleanup_lock unlocks when it should'
        gsscript.weLocked = True
        cleanup_lock()
        self.assertEqual(1, gsscript.lock.release.call_count)

    def test_cleanup_lock_untouched(self):
        'Test that cleanup_lock leaves the lock locked when it should'
        gsscript.weLocked = False
        cleanup_lock()
        self.assertEqual(0, gsscript.lock.release.call_count)
