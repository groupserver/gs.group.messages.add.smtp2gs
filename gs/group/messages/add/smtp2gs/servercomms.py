# -*- coding: utf-8 -*-
'''Utility functions for communicating to the GroupServer server.'''
##############################################################################
#
# Copyright © 2014, 2016 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals, absolute_import, print_function
from base64 import b64encode
import sys
if (sys.version_info < (3, )):
    from httplib import OK as HTTP_OK
else:
    from http.client import OK as HTTP_OK  # lint:ok
from json import loads as json_loads  # noqa: E234
from gs.form import post_multipart  # noqa: E234

#: How long to wait for the HTTP connection to time out, in seconds.
HTTP_TIMEOUT = 8  # seconds


class NotOk(Exception):
    '''Something other than a 200 OK was returned by the HTTP server.'''
    pass


#: The URI that is used to check if a group exists.
GROUP_EXISTS_URI = '/gs-group-messages-add-group-exists.html'


def get_group_info_from_address(netloc, usessl, address, token):
    '''Get the group information from an email address for the list.

:param str netloc: The name of the GroupServer host to check with.
:param bool usessl: ``True`` if TLS should be used to communicate with the
                    server.
:param str address: The email address of the list (group) to be checked.
:param str token: The authentication token to pass to GroupServer.
:raises NotOk: If the server (``hostname``) responds with something
                   other than ``200``.
:return: Information about the group.
:rtype: ``dict``

Get information about a group, by sending the parameters to
:const:`GROUP_EXISTS_URI`. The server **must** respond with a JSON object,
and this is converted to a Python object before being returned
(see :func:`json.loads`).
'''
    fields = {'form.email': address, 'form.token': token,
              'form.actions.check': 'Check'}
    status, reason, data = post_multipart(netloc, GROUP_EXISTS_URI,
                                          fields, usessl=usessl)
    if status != HTTP_OK:
        raise NotOk('%s (%d <%s>)' % (reason, status, netloc))
    retval = json_loads(data)
    return retval


#: The URI that is used to add an email message.
ADD_POST_URI = '/gs-group-messages-add-email.html'


def add_post(netloc, usessl, groupId, timeSource, emailMessage, token):
    '''Add a post to a GroupServer Group.

:param str netloc: The name of the GroupServer host to add the message to.
:param bool usessl: ``True`` if TLS should be used to communicate with the
                    server.
:param str groupId: The ID of the group to add the message to.
:param TimeSource timeSource: Where to get the time-stamp of the post.
:param str emailMessage: The entire email message to add.
:param str token: The authentication token to pass to GroupServer.
:raises NotOk: If the server (``hostname``) responds with something
               other than ``200``
:return: Nothing.

Add a post to a group, by sending the parameters to :const:`ADD_POST_URI`. The
message is base-64 encoded (see :func:`base64.b64encode`) before being sent.
'''
    # we do this to ensure we have no problems with attachments
    emailMessage = b64encode(emailMessage)
    fields = {'form.emailMessage': emailMessage, 'form.groupId': groupId,
              'form.timeSource': timeSource.name, 'form.token': token, 'form.actions.add': 'Add'}
    status, reason, data = post_multipart(netloc, ADD_POST_URI,
                                          fields, usessl=usessl)
    if status != HTTP_OK:
        raise NotOk('%s (%d <%s>)' % (reason, status, netloc))


#: The URI that is used to relay an email message to a user.
RELAY_EMAIL_URI = '/gs-profile-email-relay.html'


def relay_email(netloc, usessl, emailMessage, token):
    '''Add a post to a GroupServer Group.

:param str netloc: The name of the GroupServer host to relay the message
                   through.
:param bool usessl: ``True`` if TLS should be used to communicate with the
                    server.
:param str emailMessage: The entire email message to relay.
:param str token: The authentication token to pass to GroupServer.
:raises NotOk: If the server (``hostname``) responds with something
               other than ``200``
:return: Nothing.

Relay an email message to a user through GroupServer, by sending the parameters
to :const:`RELAY_EMAIL_URI`. The message is base-64 encoded (see
:func:`base64.b64encode`) before being sent.
'''
    # we do this to ensure we have no problems with attachments
    emailMessage = b64encode(emailMessage)
    fields = {'form.emailMessage': emailMessage,
              'form.token': token, 'form.actions.relay': 'Relay'}
    status, reason, data = post_multipart(netloc, RELAY_EMAIL_URI,
                                          fields, usessl=usessl)
    if status != HTTP_OK:
        raise NotOk('%s (%d <%s>)' % (reason, status, netloc))


#: The URI that is used to record an XVERP bounce.
BOUNCE_URI = '/gs-group-member-bounce.html'


def add_bounce(netloc, usessl, userEmailAddress, groupEmailAddress,
               token):
    '''Add a bounce to the server.

:param str netloc: The name of the GroupServer host to log the bounce with.
:param bool usessl: ``True`` if TLS should be used to communicate with the
                    server.
:param str userEmailAddress: The email address that is bouncing.
:param str groupEmailAddress: The email address of the group that sent the
                              message.
:param str token: The authentication token to pass to GroupServer.
:raises NotOk: If the server (``hostname``) responds with something
               other than ``200``
:return: Nothing.

Log a bounce with GroupServer, by sending the parameters to
:const:`BOUNCE_URI`.'''
    fields = {'form.userEmail': userEmailAddress,
              'form.groupEmail': groupEmailAddress,
              'form.token': token, 'form.actions.handle': 'Handle'}
    status, reason, data = post_multipart(netloc, BOUNCE_URI,
                                          fields, usessl=usessl)
    if status != HTTP_OK:
        raise NotOk('%s (%d <%s>)' % (reason, status, netloc))
