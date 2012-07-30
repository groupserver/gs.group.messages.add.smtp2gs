# coding=utf-8
import re
from urlparse import urlparse
from servercomms import get_group_info_from_address, add_bounce

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
