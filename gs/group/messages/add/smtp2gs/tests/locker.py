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
from mock import MagicMock
from os import remove, stat
from tempfile import NamedTemporaryFile
from unittest import TestCase
import gs.group.messages.add.smtp2gs.locker as smtp2gs_locker


class TestLocker(TestCase):

    def setUp(self):
        self.oldLockName = smtp2gs_locker.LOCK_NAME
        with NamedTemporaryFile('w') as tmp:
            smtp2gs_locker.LOCK_NAME = tmp.name
        self.del_lock()

    def del_lock(self):
        try:
            remove(smtp2gs_locker.LOCK_NAME)
        except OSError:
            pass

    def tearDown(self):
        self.del_lock()
        smtp2gs_locker.LOCK_NAME = self.oldLockName

    def test_create_file(self):
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        s = stat(smtp2gs_locker.LOCK_NAME)
        self.assertEqual(s.st_size, 82)

    def test_age(self):
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        a = smtp2gs_locker.age(smtp2gs_locker.LOCK_NAME)
        self.assertGreaterEqual(a, 0)

    def test_get_lock_new_lock_locked(self):
        self.del_lock()
        lock = smtp2gs_locker.get_lock()
        self.assertTrue(lock.i_am_locking())
