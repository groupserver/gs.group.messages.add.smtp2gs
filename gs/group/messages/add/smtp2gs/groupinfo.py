# coding=utf-8
from httplib import OK as HTTP_OK
from json import loads as json_loads
from gs.form import post_multipart

class NotOk(Exception):
    pass

GROUP_EXISTS_URI = '/gs-group-messages-add-group-exists.html'

def get_group_info_from_address(hostname, address):
    fields = {'form.email': address, 'form.token': 'foo',
              'form.actions.check': 'Check'}
    status, reason, data = post_multipart(hostname, 
                                          GROUP_EXISTS_URI, fields) # port?
    if status != HTTP_OK:
        raise NotOk('%s (%d)' % (reason, status))

    retval = json_loads(data)
    return retval
