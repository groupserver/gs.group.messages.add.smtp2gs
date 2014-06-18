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
from mock import patch
from multiprocessing import Process
from os import remove, stat
from tempfile import NamedTemporaryFile
from time import time, sleep
from unittest import TestCase
from lockfile import FileLock
import gs.group.messages.add.smtp2gs.locker as smtp2gs_locker


class TestLocker(TestCase):
    '''Test the file-locking code'''
    def setUp(self):
        self.oldLockName = smtp2gs_locker.LOCK_NAME
        self.oldBreakLockTimeout = smtp2gs_locker.BREAK_LOCK_AGE
        self.maxLockTimeout = smtp2gs_locker.MAX_LOCK_TIMEOUT
        with NamedTemporaryFile('w', delete=False) as tmp:
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

    def assertLocking(self, lock):
        self.assertTrue(lock.i_am_locking(), 'Not locking')

    def assertUnlocked(self, lock):
        self.assertFalse(lock.i_am_locking(), 'Locking')

    def test_create_file(self):
        'Test the call to create_file'
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        s = stat(smtp2gs_locker.LOCK_NAME)
        self.assertEqual(s.st_size, 82)

    def test_age(self):
        'Test the function that gets the age of a file'
        smtp2gs_locker.create_file(smtp2gs_locker.LOCK_NAME)
        a = smtp2gs_locker.age(smtp2gs_locker.LOCK_NAME)
        self.assertGreaterEqual(a, 0)

    def test_get_lock_new_lock_locked(self):
        '''Test that a new process will acquire a lock'''
        lock = smtp2gs_locker.get_lock()
        self.assertLocking(lock)

    def test_get_lock_new_lock_not_locked(self):
        '''Test that a second process will not gain the lock,
        but it will time-out waiting for the lock, and end up with nothing.'''
        # --=mpj17=-- Using timeouts ain't pretty, but it works for 22:33.
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
        self.assertUnlocked(l2)
        diff = t2 - t1
        # Assert that we waited the correct amount of time.
        self.assertGreaterEqual(diff, smtp2gs_locker.MAX_LOCK_TIMEOUT)
        self.assertLess(diff, smtp2gs_locker.MAX_LOCK_TIMEOUT * 2)

        # Wait for the badly behaved subprocess
        p.join()

    def test_get_lock_break_lock(self):
        '''Test the breaking of the lock, if a process has held it too long.'''
        smtp2gs_locker.BREAK_LOCK_AGE = 3  # seconds
        smtp2gs_locker.MAX_LOCK_TIMEOUT = 2  # seconds
        self.assertTrue(True)

        # Start a "badly behaved" subprocess, that will gain the lock.
        t = smtp2gs_locker.BREAK_LOCK_AGE * 3
        p = Process(target=get_lock, args=(t, ))
        p.start()

        # Wait for the lock to be acquired by the badly behaved subprocess
        sleep(smtp2gs_locker.BREAK_LOCK_AGE)

        # Try and get the lock.
        l2 = smtp2gs_locker.get_lock()

        # Assert that we have the lock, because the lock has been broken
        self.assertLocking(l2)

        # Wait for the badly behaved subprocess
        p.join()


def get_lock(t):
    '''A function that pretends to be a badly behaved subprocess

    :param int t: Time to sleep with the lock acquired (seconds)'''
    smtp2gs_locker.get_lock()
    sleep(t)
