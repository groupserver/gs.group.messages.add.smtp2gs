# coding=utf-8
# Standard modules
from argparse import ArgumentParser, FileType, Action
from email import message_from_string
from socket import gaierror
import sys
from urlparse import urlparse
# GroupServer modules
from gs.config.config import Config, ConfigError
# Local modules
from locker import get_lock
from servercomms import get_group_info_from_address, NotOk, add_post

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
    'locked':                EX_TEMPFAIL,
    'no_x_original_to':      EX_DATAERR,
    'json_decode_error':     EX_PROTOCOL,
    'no_group':              EX_NOUSER,}

def add_post_to_groupserver(progName, url, listId, emailMessage, token):
    # First, get the lock or die!!
    lock = get_lock()
    if not lock.i_am_locking():
        m = '%s: Not processing the email message of %d bytes as %s is '\
            'locked.\n' % (progName, len(emailMessage), progName)
        sys.stderr.write(m)
        sys.exit(exit_vals['locked']) # Postfix will try again later

    parsedUrl = urlparse(url)
    if not parsedUrl.hostname:
        m = '%s: No host in the URL <%s>\n' % (p.prog, args.url)
        sys.stderr.write(m)
        sys.exit(exit_vals['url_bung'])

    if listId:
        groupToSendTo = listId
    else:
        # Figure out if the group exists.
        email = message_from_string(emailMessage)
        xOriginalTo = email['x-original-to']
        if xOriginalTo == None:
            m = '%s: No "x-original-to" header in the email message.\n' \
                % (progName)
            sys.stderr.write(m)
            sys.exit(exit_vals['no_x_original_to'])
            
        # Get the information about the group
        try:
            groupInfo = get_group_info_from_address(parsedUrl.hostname,
                                                    xOriginalTo, token)
        except gaierror, g:
            m = '%s: Error connecting to <%s> while looking up the group '\
                'information:\n%s:    %s\n' %  (progName, url, progName, g)
            sys.stderr.write(m)
            sys.exit(exit_vals['socket_error'])
        except NotOk, ne:
            m = '%s: Issue communicating with the server while looking up the '\
                'group information:\n%s    %s\n' % (progName, progName, ne)
            sys.stderr.write(m)
            sys.exit(exit_vals['communication_failure'])
        except ValueError, ve:
            m = '%s: Could not decode the data returned by the server while '\
                'looking up the \n%s: group information. Check the token.\n' %\
                (progName, progName)
            sys.stderr.write(m)
            sys.exit(exit_vals['json_decode_error'])
            
        groupToSendTo = groupInfo['groupId']

    if not(groupToSendTo):
        m = '%s: There is no group to send the email message to.' % progName
        sys.stderr.write(m)
        sys.exit(exit_vals['no_group'])
        
    # Finally, add the email to the group.
    try:
        add_post(parsedUrl.hostname, groupToSendTo, emailMessage, token)
    except gaierror, g:
        m = '%s: Error connecting to <%s> while adding the email message:\n'\
            '%s:    %s\n' %  (progName, url, progName, g)
        sys.stderr.write(m)
        sys.exit(exit_vals['socket_error'])
    except NotOk, ne:
        m = '%s: Issue communicating with the server while adding the email '\
            'message:\n%s    %s\n' % (progName, progName, ne)
        sys.stderr.write(m)
        sys.exit(exit_vals['communication_failure'])
    
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
        m = '%s: Configuration error for the file "%s":\n' \
            '%s: %s\n' % (p.prog, args.config, p.prog, ce.message)
        sys.stderr.write(m)
        sys.exit(exit_vals['config_error'])

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

    add_post_to_groupserver(p.prog, args.url, args.listId, emailMessage, token)
    sys.exit(0)

if __name__ == '__main__':
    main('etc/gsconfig.ini')
