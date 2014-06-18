# -*- coding: utf-8 -*-
'''Get a lock-file, to slow down the addition of messages by SMTP. Based on
:class:`lockfile.FileLock`.'''
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

#: The name of the lock-file.
LOCK_NAME = '/tmp/gs-group-messages-add-smtp2gs'

#: The time to wait for the lock to become avaliable, in seconds.
MAX_LOCK_TIMEOUT = 5  # seconds

#: How old the lock must be, in seconds, before it is broken.
BREAK_LOCK_AGE = 300  # seconds == 5 minutes


def get_lock():
    '''Get a file-lock, breaking the lock if it has been held for too long.

:return: A lock, which may be locked. Use the
         :meth:`lockfile.FileLock.i_am_locking` method to find out if the
         lock is held, or not.
:rtype: :class:`lockfile.FileLock`

It is more than possible for Postfix to consume every single thread on the
sever. By adding a lock, with a short timeout, we slow down the consumption of
threads by the asynchronous email UI; this allows the Web UI to be responsive.

We break the lock if the lock is very old because it is more than possible for
something to crash with the lock taken. (It does assume that no email will
take more than :const:`BREAK_LOCK_AGE` to process.)

If the file is still locked, after we wait for something to finish and check
that the lock is not too old, then we exit. Postfix will try running the
script with the same arguments again later.

**Example**::

    from gs.group.messsages.add.smtp2gs import locker
    lock = locker.get_lock()
    if lock.i_am_locking():
        # Do stuff.
'''
    # TODO: Use Redis for the locking
    # (We have the config for Redis in the config file)

    create_file(LOCK_NAME)
    # The following is a modification of the example from the lockfile
    # documentation <http://packages.python.org/lockfile/lockfile.html>
    lock = FileLock(LOCK_NAME)
    lock_file = LOCK_NAME + '.lock'
    if not lock.i_am_locking():
        if (isfile(lock_file) and (age(lock_file) >= BREAK_LOCK_AGE)):
            lock.break_lock()

    try:
        lock.acquire(timeout=MAX_LOCK_TIMEOUT)
    except LockTimeout:
        pass
    return lock


def create_file(fileName):
    '''Create the lock file.

    :param str fileName: The name of the lock file.
    :return: Nothing.'''
    if not isfile(fileName):
        with open(fileName, 'w') as f:
            m = 'This file is part of the locking mechanism used by the '\
                'GroupServer smtp2gs\nscript.'
            f.write(m)


def age(fileName):
    '''Get the age of a file.

    :param str fileName: The name of the file to check.
    :return: The age of the file, in seconds.
    :rtype: ``int``
'''
    mTime = getmtime(fileName)
    retval = time() - mTime
    assert retval >= 0
    return retval
