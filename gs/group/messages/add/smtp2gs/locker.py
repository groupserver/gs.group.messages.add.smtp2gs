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
from __future__ import unicode_literals
from lockfile import FileLock, LockTimeout
from os.path import getmtime, isfile
from time import time

LOCK_NAME = '/tmp/gs-group-messages-add-smtp2gs'
LOCK_FILE = LOCK_NAME + '.lock'
MAX_LOCK_TIMEOUT = 5  # seconds
BREAK_LOCK_AGE = 300  # seconds == 5 minutes


def get_lock():
    '''Get the lock for smtp2gs, breaking the lock if it has been held for too
long.

Arguments:
  None

Returns:
  A ``lockfile.FileLock``, which may be locked. Use the method
  ``lockfile.FileLock.i_am_locking`` to find out.'''

    create_file(LOCK_NAME)
    # The following is a modification of the example from the lockfile
    # documentation <http://packages.python.org/lockfile/lockfile.html>
    #
    # The reason this locking is here is that it is more than possible for
    # Postfix to consume every single thread on the sever. By adding a
    # lock, with a short timeout, we slow down the consumption of threads
    # by the asynchronous email UI; this prevents the Web UI (which needs
    # to be responsive) from locking up.
    #
    # We break the lock if the lock is very old because it is more than
    # possible for something to crash with the lock taken. (It does assume
    # that no email will take more than BREAK_LOCK_AGE to process.)
    #
    # If the file is still locked, after we wait for something to finish
    # and check that the lock is not too old, then we exit. Postfix will
    # try running the script with the same arguments again later.
    lock = FileLock(LOCK_NAME)
    if not lock.i_am_locking():
        if (isfile(LOCK_FILE) and (age(LOCK_FILE) > BREAK_LOCK_AGE)):
            lock.break_lock()

    try:
        lock.acquire(timeout=MAX_LOCK_TIMEOUT)
    except LockTimeout:
        pass
    return lock


def create_file(fileName):
    if not isfile(fileName):
        with open(fileName, 'w') as f:
            m = 'This file is part of the locking mechanism used by the '\
                'GroupServer smtp2gs\nscript.'
            f.write(m)


def age(fileName):
    mTime = getmtime(fileName)
    retval = time() - mTime
    assert retval >= 0
    return retval
