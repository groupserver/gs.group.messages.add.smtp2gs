# coding=utf-8
# Standard modules
from argparse import ArgumentParser, FileType, Action
from email import message_from_string
from socket import gaierror
import sys
from urlparse import urlparse
# Local modules
from locker import get_lock
from groupinfo import get_group_info_from_address, NotOk

exit_vals = {
    'success':                0,
    'input_file_empty':      10,
    'input_file_too_large':  11,
    'url_bung':              20,
    'communication_failure': 21,
    'socket_error':          22,
    'locked':                30,
    'no_x_original_to':      40,
    'json_decode_error':     50,}

HTTP_TIMEOUT = 8 # seconds

def add_post_to_groupserver(progName, url, emailMessage):
    # Get lock or die!!
    lock = get_lock()
    if not lock.i_am_locking():
        m = '%s: Not processing the email message of %d bytes as %s is '\
            'locked.\n' % (progName, len(emailMessage), progName)
        sys.stderr.write(m)
        sys.exit(exit_vals['locked']) # Postfix will try again later

    email = message_from_string(emailMessage)
    parsedUrl = urlparse(url)

    # First, figure out if the group exists.
    xOriginalTo = email['x-original-to']
    if xOriginalTo == None:
        m = '%s: No "x-original-to" header in the email message.\n' % (progName)
        sys.stderr.write(m)
        sys.exit(exit_vals['no_x_original_to'])

    try:
        groupInfo = get_group_info_from_address(parsedUrl.hostname, xOriginalTo)
    except gaierror, g:
        m = '%s: Error connecting to <%s>:\n%s:    %s\n' % \
            (progName, url, progName, g)
        sys.stderr.write(m)
        sys.exit(exit_vals['socket_error'])
    except NotOk, ne:
        m = '%s: Issue communicating with the server: %s \n' \
            % (progName, ne)
        sys.stderr.write(m)
        sys.exit(exit_vals['communication_failure'])
    except ValueError, ve:
        m = '%s: Could not decode the data returned by the server.\n' \
            % (progName)
        sys.stderr.write(m)
        sys.exit(exit_vals['json_decode_error'])

    print groupInfo

    ## VVVVVVVVVVVVVVVVVVVVVVVVVV ##
    ## vvvvvvvvvvvvvvvvvvvvvvvvvv ##
    lock.release() # Very important!
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
    ## AAAAAAAAAAAAAAAAAAAAAAAAAA ##

def MiB_to_B(mb):
    retval = mb * (2**20)
    assert retval > mb
    return retval

def main(configFileName):
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
        sys.exit(exit_vals['input_file_empty'])
    elif (MiB_to_B(args.maxSize) < l):
        m = '%s: Email message too large (%d bytes, rather than %d '\
            'bytes).\n' % (p.prog, len(emailMessage), MiB_to_B(args.maxSize))
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_too_large'])

    url = urlparse(args.url)
    if not url.hostname:
        m = '%s: No host in the URL <%s>\n' % (p.prog, args.url)
        sys.stderr.write(m)
        sys.exit(exit_vals['url_bung'])

    add_post_to_groupserver(p.prog, args.url, emailMessage)
    sys.exit(0)
if __name__ == '__main__':
    main()
