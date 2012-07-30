# coding=utf-8
# Standard modules
from argparse import ArgumentParser, FileType, Action
import atexit
from email import message_from_string
from socket import gaierror
import sys
from urlparse import urlparse
# GroupServer modules
from gs.config.config import Config, ConfigError
# Local modules
from locker import get_lock
from servercomms import get_group_info_from_address, NotOk, add_post

weLocked = False
lock = None

# See /usr/include/sysexits.h
EX_OK       =  0
EX_USAGE    = 64
EX_DATAERR  = 65
EX_NOUSER   = 67
EX_PROTOCOL = 76
EX_TEMPFAIL = 75
EX_CONFIG   = 78
exit_vals = {
    'success':               EX_OK,
    'input_file_empty':      EX_DATAERR,
    'input_file_too_large':  EX_DATAERR,
    'config_error':          EX_CONFIG,
    'url_bung':              EX_USAGE,
    'communication_failure': EX_PROTOCOL,
    'socket_error':          EX_PROTOCOL,
    'locked':                EX_TEMPFAIL, # Postfix will try again later
    'no_x_original_to':      EX_DATAERR,
    'json_decode_error':     EX_PROTOCOL,
    'no_group':              EX_NOUSER,}

# The error-messages that are written to STDERR conform to RFC 3463
# <http://tools.ietf.org/html/rfc3463>. If a problem can be changed with an
# alteration to the configuration then a 4.x.x error will be returned.

# XVERP addresses look like listId+userMailbox=user.domain@this.server
XVERP_RE = re.compile('(.*?)\+(.*?)\=(.*?)\@(.*)')
def is_an_xverp_bounce(toAddress):
    result = XVERP_RE.search(toAddress)
    retval = result and (len(result.groups()) == 4)
    assert type(retval) == bool
    return retval

def handle_bounce(hostname, toAddress, token):
    groups = XVERP_RE.search(toAddress).groups()
    listAddress = '@'.join((groups[0], groups[3])) # listId@this.server
    userAddress = '@'.join((groups[1], groups[2])) # userMailbox@user.domain

    groupInfo = get_group_info_from_address(hostname, listAddress, token)
    host = urlparse(groupInfo['siteUrl'])[1]
    add_bounce(host, userAddress, groupInfo['groupId'], token)

def add_post_to_groupserver(progName, url, listId, emailMessage, token):
    # WARNING: multiple exit points below thanks to "sys.exit" calls. Dijkstra 
    # will hate me for this.

    # First, get the lock or die!!
    global weLocked, lock 
    lock = get_lock()
    if not lock.i_am_locking():
        m = '4.4.5 Not processing the message, as the system is too busy.'
        sys.stderr.write(m)
        sys.exit(exit_vals['locked'])
    weLocked = True

    parsedUrl = urlparse(url)
    if not parsedUrl.hostname:
        m = '4.5.2 No host in the URL <%s>\n' % (url)
        sys.stderr.write(m)
        sys.exit(exit_vals['url_bung'])
    hostname = parsedUrl.hostname

    if listId:
        groupToSendTo = listId
    else:
        # Figure out if the group exists.
        email = message_from_string(emailMessage)
        xOriginalTo = email['x-original-to']
        if xOriginalTo == None:
            m = '5.1.3 No "x-original-to" header in the email message.\n' 
            sys.stderr.write(m)
            sys.exit(exit_vals['no_x_original_to'])
            
        # Check for a XVERP bounce
        if is_an_xverp_bounce(xOriginalTo):
            try:
                handle_bounce(hostname, xOriginalTo, token)
            except gaierror, g:
                m = '4.4.4 Error connecting to the server while processing '\
                    'the XVERP bounce:\n%s\n' %  (g)
                sys.stderr.write(m)
                sys.exit(exit_vals['socket_error'])
            except NotOk, ne:
                m = '4.5.0 Error communicating with the server while '\
                    'processing the XVERP bounce:\n%s\n' % (ne)
                sys.stderr.write(m)
                sys.exit(exit_vals['communication_failure'])
            except ValueError, ve:
                m = '4.5.0 Could not decode the data returned by the server '\
                    'while processing the \nXVERP bounce. Check the token?\n'
                sys.stderr.write(m)
                sys.exit(exit_vals['json_decode_error'])
            else:            
                m = '2.1.5 The XVERP bounce was processed.'
                sys.stderr.write(m)
                sys.exit(exit_vals['success'])
            
        # Get the information about the group
        try:
            groupInfo = get_group_info_from_address(hostname, xOriginalTo, 
                                                    token)
        except gaierror, g:
            m = '4.4.4 Error connecting to <%s> while looking up the group '\
                'information:\n%s\n' %  (url, g)
            sys.stderr.write(m)
            sys.exit(exit_vals['socket_error'])
        except NotOk, ne:
            m = '4.5.0 Error communicating with the server while looking up '\
                'the group information:\n%s\n' % (ne)
            sys.stderr.write(m)
            sys.exit(exit_vals['communication_failure'])
        except ValueError, ve:
            m = '4.5.0 Could not decode the data returned by the server while '\
                'looking up the \ngroup information. Check the token?\n'
            sys.stderr.write(m)
            sys.exit(exit_vals['json_decode_error'])
            
        groupToSendTo = groupInfo['groupId']

    if not(groupToSendTo):
        m = '5.1.1 There is no such group on this site.'
        sys.stderr.write(m)
        sys.exit(exit_vals['no_group'])
        
    # Finally, add the email to the group.
    try:
        add_post(hostname, groupToSendTo, emailMessage, token)
    except gaierror, g:
        m = '4.4.4 Error connecting to <%s> while adding the message:\n%s\n' %\
            (url, g)
        sys.stderr.write(m)
        sys.exit(exit_vals['socket_error'])
    except NotOk, ne:
        m = '4.5.0 Issue communicating with the server while adding the '\
            'message:\n    %s\n' % (ne)
        sys.stderr.write(m)
        sys.exit(exit_vals['communication_failure'])

@atexit.register
def cleanup_lock():
    global weLocked, lock
    if weLocked:
        ## VVVVVVVVVVVVVVVVVVVVVVVVVV ##
        ## vvvvvvvvvvvvvvvvvvvvvvvvvv ##
        lock.release() # Very important!
        ## ^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
        ## AAAAAAAAAAAAAAAAAAAAAAAAAA ##

def MiB_to_B(mb):
    retval = mb * (2**20)
    assert retval > mb
    return retval

def get_token_from_config(configSet, configFileName):
    config = Config(configSet, configFileName)
    config.set_schema('webservice', {'token': str})
    ws = config.get('webservice')
    retval = ws['token']
    if not retval:
        m = 'The token was not set.'
        raise ValueError(m)
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
    p.add_argument('-l', '--list', dest='listId', default=None,
                   help='The list to send the message to. By default it is '\
                       'extracted from the x-original-to header.')
    p.add_argument('-f', '--file', dest='file', default='-', 
                   type=FileType('r'),
                   help='The name of the file that contains the message. If '\
                       'omitted (or "%(default)s") standard-input will be '\
                       'read.')
    p.add_argument('-c', '--config', dest='config', default=configFileName,
                   type=str,
                   help='The name of the GroupServer configuration file '\
                       '(default "%(default)s") that contains the token that '\
                       'will be used to authenticate the script when it tries '\
                       'to add the email to the site.')
    p.add_argument('-i','--instance', dest='instance', default='default',
                   type=str,
                   help = 'The identifier of the GroupServer instance '\
                       'configuration to use (default "%(default)s").')
    args = p.parse_args()
    
    try:
        token = get_token_from_config(args.instance, args.config)
    except ConfigError, ce:
        m = '4.3.5: Error with the configuration file "%s":\n%s\n' %\
            (args.config, ce.message)
        sys.stderr.write(m)
        sys.exit(exit_vals['config_error'])

    emailMessage = args.file.read()
    args.file.close()
    l = len(emailMessage)
    if l == 0:
        m = '5.3.0 The file containing the email was empty.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_empty'])
    elif (MiB_to_B(args.maxSize) < l):
        m = '5.3.4 Email message too large (%d bytes, rather than %d '\
            'bytes).\n' % (len(emailMessage), MiB_to_B(args.maxSize))
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_too_large'])
    
    add_post_to_groupserver(p.prog, args.url, args.listId, emailMessage, token)
    sys.exit(exit_vals['success'])
    
if __name__ == '__main__':
    main('etc/gsconfig.ini')
