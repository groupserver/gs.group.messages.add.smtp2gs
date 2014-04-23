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
from multiprocessing import Process
from os import remove, stat
from tempfile import NamedTemporaryFile
from time import time, sleep
from unittest import TestCase
from lockfile import FileLock
import gs.group.messages.add.smtp2gs.locker as smtp2gs_locker


class TestLocker(TestCase):

    def setUp(self):
        self.oldLockName = smtp2gs_locker.LOCK_NAME
        self.oldBreakLockTimeout = smtp2gs_locker.BREAK_LOCK_AGE
        self.maxLockTimeout = smtp2gs_locker.MAX_LOCK_TIMEOUT
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
        fl = FileLock(smtp2gs_locker.LOCK_NAME)
        fl.break_lock()
        smtp2gs_locker.LOCK_NAME = self.oldLockName
        smtp2gs_locker.BREAK_LOCK_AGE = self.oldBreakLockTimeout
        smtp2gs_locker.MAX_LOCK_TIMEOUT = self.maxLockTimeout

    def test_create_file(self):
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        s = stat(smtp2gs_locker.LOCK_NAME)
        self.assertEqual(s.st_size, 82)

    def test_age(self):
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        a = smtp2gs_locker.age(smtp2gs_locker.LOCK_NAME)
        self.assertGreaterEqual(a, 0)

    def test_get_lock_new_lock_locked(self):
        '''Test that a new process will acquire a lock'''
        self.del_lock()
        lock = smtp2gs_locker.get_lock()
        self.assertTrue(lock.i_am_locking())

    def test_get_lock_new_lock_not_locked(self):
        '''Test that a second process will not gain the lock, but it will
        time-out waiting for the lock, and end up with nothing.'''
        # --=mpj17=-- Using timeouts ain't pretty, but it works for 22:33.
        self.del_lock()
        smtp2gs_locker.MAX_LOCK_TIMEOUT = 2  # seconds

        # Start a "badly behaved" subprocess, that will gain the lock.
        t = smtp2gs_locker.MAX_LOCK_TIMEOUT * 3
        p = Process(target=get_lock, args=(t, ))
        p.start()
        # Wait for the lock to be acquired by the badly behaved subprocess
        sleep(smtp2gs_locker.MAX_LOCK_TIMEOUT / 2)

        # Try and get the lock.
        t1 = time()
        l2 = smtp2gs_locker.get_lock()
        t2 = time()

        # Assert that we have not got the lock
        self.assertFalse(l2.i_am_locking())
        diff = t2 - t1
        # Assert that we waited the correct amount of time.
        self.assertGreaterEqual(diff, smtp2gs_locker.MAX_LOCK_TIMEOUT)
        self.assertLess(diff, smtp2gs_locker.MAX_LOCK_TIMEOUT * 2)

        # Wait for the badly behave subprocess
        p.join()

    def test_get_lock_break_lock(self):
        smtp2gs_locker.BREAK_LOCK_AGE = 3
        self.del_lock()
        self.assertTrue(True)


def get_lock(t):
    # Pretend to be a badly behaved subprocess.
    smtp2gs_locker.get_lock()
    sleep(t)
