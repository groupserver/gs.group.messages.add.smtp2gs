# coding=utf-8
from argparse import ArgumentParser, FileType, Action

def get_args(configFileName)
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
    retval = p.parse_args()
    return retval
