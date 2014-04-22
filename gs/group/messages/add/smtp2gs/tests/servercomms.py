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
from mock import MagicMock
from json import dumps as to_json
from unittest import TestCase
import gs.group.messages.add.smtp2gs.servercomms as smtp2gs_servercomms


class TestServerComms(TestCase):
    def setUp(self):
        pageContent = to_json({'foo': 'bar'})
        r = (smtp2gs_servercomms.HTTP_OK, 'Ok', pageContent)
        smtp2gs_servercomms.post_multipart = MagicMock(return_value=r)

    def test_get_group_info_from_address(self):
        smtp2gs_servercomms.get_group_info_from_address('gstest',
            'development@groupserver.org', 'token', True)
        self.assertEqual(1, smtp2gs_servercomms.post_multipart.call_count)
        args, kw_args = smtp2gs_servercomms.post_multipart.call_args
        self.assertEqual('gstest', args[0])
        self.assertEqual(smtp2gs_servercomms.GROUP_EXISTS_URI, args[1])
        fields = args[2]
        self.assertIn('form.email', fields)
        self.assertEqual(fields['form.email'], 'development@groupserver.org')
        self.assertIn('form.token', fields)
        self.assertIn('form.actions.check', fields)
        self.assertTrue(kw_args['usessl'])
