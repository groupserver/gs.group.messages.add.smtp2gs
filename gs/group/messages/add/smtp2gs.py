# coding=utf-8
from argparse import ArgumentParser, FileType, Action
from lockfile import FileLock, LockTimeout
from os import utime
from os.path import getmtime
import sys
from time import time

LOCK_FILE_NAME   = '/tmp/gs-group-messages-add-smtp2gs.lock'
MAX_LOCK_TIMEOUT =   5 # seconds
BREAK_LOCK_AGE   = 300 # seconds == 5 minutes

def add_post_to_groupserver(url, emailMessage):
    create_file(LOCK_FILE_NAME)
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
    # possible for something to crash, and to leave the lock taken. (It
    # does assume that no email will take more than BREAK_LOCK_AGE to
    # process.)
    #
    # If the file is still locked, after we wait for something to finish
    # and check that the lock is not too old, then we exit. Postfix will
    # try running the script with the same arguments again later.
    lock = FileLock(LOCK_FILE_NAME)
    while not lock.i_am_locking():
        try:
            lock.acquire(timeout=MAX_LOCK_TIMEOUT)
        except LockTimeout:
            if age(LOCK_FILE_NAME) > BREAK_LOCK_AGE:
                lock.break_lock()
            else:
                sys.exit(20) # Postfix will try again later
        touch(LOCK_FILE_NAME)
        lock.acquire()

def create_file(fileName):
    f = file(fileName, 'w')
    f.close()

def age(fileName):
    mTime = getmtime(fileName)
    retval = time() - mTime
    assert retval >= 0
    return retval

def touch(fileName):
    now = time()
    utime(fileName, (now, now))

def MiB_to_B(mb):
    retval = mb * (2**20)
    assert retval > mb
    return retval

def main():
    p = ArgumentParser(description='Add an email message to GroupServer.',
                       epilog='Usually %(prog)s is called by a SMTP server '\
                           '(such as Postfix) in order to add an email '\
                           'message to a GroupServer group.')
    p.add_argument('url', metavar='url', 
                   help='The URL for the GroupServer site.')
    p.add_argument('-m', '--max-size', dest='maxSize', type=int, default=200,
                   help='The maximum size of the post that will be accepted, '\
                       'in mebibytes (default %(default)sMiB).')
    p.add_argument('-l', '--list', dest='listId',
                   help='The list to send the message to. By default it is '\
                       'extracted from the x-original-to header.')
    p.add_argument('-f', '--file', dest='file', default='-', 
                   type=FileType('r'),
                   help='The name of the file that contains the message. If '\
                       'omitted (or "%(default)s") standard-input will be '\
                       'read.') 
    args = p.parse_args()
    
    emailMessage = args.file.read()
    args.file.close()
    l = len(emailMessage)
    if l == 0:
        m = '%s: The file containing the email was empty.\n' % p.prog
        sys.stderr.write(m)
        sys.exit(10)
    elif (MiB_to_B(args.maxSize) < l):
        m = '%s: Email message too large (%d bytes, rather than %d '\
            'bytes).\n' % (p.prog, len(emailMessage), MiB_to_B(args.maxSize))
        sys.stderr.write(m)
        sys.exit(11)

    add_post_to_groupserver(args.url, emailMessage)
    sys.exit(0)
if __name__ == '__main__':
    main()
