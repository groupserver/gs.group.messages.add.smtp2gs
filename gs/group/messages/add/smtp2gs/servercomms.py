# coding=utf-8
from httplib import OK as HTTP_OK
from json import loads as json_loads
from gs.form import post_multipart

HTTP_TIMEOUT = 8 # seconds

class NotOk(Exception):
    pass

GROUP_EXISTS_URI = '/gs-group-messages-add-group-exists.html'

def get_group_info_from_address(hostname, address, token):
    fields = {'form.email': address, 'form.token': token,
              'form.actions.check': 'Check'}
    status, reason, data = post_multipart(hostname, GROUP_EXISTS_URI, 
                                          fields) # port?
    if status != HTTP_OK:
        raise NotOk('%s (%d)' % (reason, status))

    retval = json_loads(data)
    return retval

ADD_POST_URI = '/gs-group-messages-add-email.html'
def add_post(hostname, groupId, emailMessage, token):
    fields = {'form.emailMessage': emailMessage, 'form.groupId': groupId,
              'form.token': token, 'form.actions.add': 'Add'}
    status, reason, data = post_multipart(hostname, ADD_POST_URI, 
                                          fields) # port?
    if status != HTTP_OK:
        raise NotOk('%s (%d)' % (reason, status))
