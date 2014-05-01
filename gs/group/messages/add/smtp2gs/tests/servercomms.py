# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from base64 import b64encode
from mock import MagicMock
from json import dumps as to_json
from unittest import TestCase
import gs.group.messages.add.smtp2gs.servercomms as smtp2gs_servercomms


class TestServerComms(TestCase):
    'Tests for server communications.'
    def setUp(self):
        pageContent = to_json({'foo': 'bar'})
        self.ok = (smtp2gs_servercomms.HTTP_OK, 'Ok', pageContent)
        self.fail = (500, 'So very not ok', pageContent)

    def check_field(self, fields, fieldId, expected):
        self.assertIn(fieldId, fields)
        self.assertEqual(fields[fieldId], expected)

    def test_get_group_info_from_address(self):
        'Test the call to get_group_info_from_address'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.ok)
        smtp2gs_servercomms.get_group_info_from_address('gstest', True,
            'development@groupserver.org', 'token')
        self.assertEqual(1, smtp2gs_servercomms.post_multipart.call_count)
        args, kw_args = smtp2gs_servercomms.post_multipart.call_args
        self.assertEqual('gstest', args[0])
        self.assertEqual(smtp2gs_servercomms.GROUP_EXISTS_URI, args[1])
        fields = args[2]
        self.check_field(fields, 'form.email', 'development@groupserver.org')
        self.check_field(fields, 'form.token', 'token')
        self.assertIn('form.actions.check', fields)
        self.assertTrue(kw_args['usessl'])

    def test_get_group_info_from_address_fail(self):
        'Test a communications issue with get_group_info_from_address'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.fail)
        self.assertRaises(smtp2gs_servercomms.NotOk,
            smtp2gs_servercomms.get_group_info_from_address,
            'gstest', True, 'development@groupserver.org', 'token')

    def test_add_post(self):
        'Test adding a post'
        hostname = 'gstest'
        group = 'development'
        message = b'I am a fish'  # Note: a byte-string
        token = 'token'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.ok)
        smtp2gs_servercomms.add_post(hostname, True, group, message, token)
        self.assertEqual(1, smtp2gs_servercomms.post_multipart.call_count)
        args, kw_args = smtp2gs_servercomms.post_multipart.call_args
        self.assertEqual(hostname, args[0])
        self.assertEqual(smtp2gs_servercomms.ADD_POST_URI, args[1])
        fields = args[2]
        self.check_field(fields, 'form.groupId', group)
        self.check_field(fields, 'form.token', token)
        self.check_field(fields, 'form.emailMessage', b64encode(message))
        self.assertIn('form.actions.add', fields)
        self.assertTrue(kw_args['usessl'])

    def test_add_post_fail(self):
        'Test a communications issue with adding a post.'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.fail)
        self.assertRaises(smtp2gs_servercomms.NotOk,
            smtp2gs_servercomms.add_post,
            'gstest', True, 'development', b'I am a fish', 'token')

    def test_add_bounce(self):
        'Test recording a bounce.'
        hostname = 'gstest'
        userEmail = 'mpj17@onlinegroups.net'
        groupEmail = 'development@groupserver.org'
        token = 'token'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.ok)
        smtp2gs_servercomms.add_bounce(hostname, True, userEmail, groupEmail,
                                        token)
        self.assertEqual(1, smtp2gs_servercomms.post_multipart.call_count)
        args, kw_args = smtp2gs_servercomms.post_multipart.call_args
        self.assertEqual(hostname, args[0])
        self.assertEqual(smtp2gs_servercomms.BOUNCE_URI, args[1])
        fields = args[2]
        self.check_field(fields, 'form.userEmail', userEmail)
        self.check_field(fields, 'form.groupEmail', groupEmail)
        self.check_field(fields, 'form.token', token)
        self.assertIn('form.actions.handle', fields)
        self.assertTrue(kw_args['usessl'])

    def test_add_bounce_fail(self):
        'Test a communications issue with adding a bounce'
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=self.fail)
        userEmail = 'mpj17@onlinegroups.net'
        groupEmail = 'development@groupserver.org'
        self.assertRaises(smtp2gs_servercomms.NotOk,
            smtp2gs_servercomms.add_bounce,
            'gstest', True, userEmail, groupEmail, 'token')
