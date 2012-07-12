# coding=utf-8
from argparse import ArgumentParser, FileType, Action
from lockfile import FileLock, LockTimeout
import sys

def add_post_to_groupserver(url, emailMessage):
    pass

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

if __name__ == '__main__':
    main()
