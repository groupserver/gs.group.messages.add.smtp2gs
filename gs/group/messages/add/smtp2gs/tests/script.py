# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from mock import (MagicMock, patch)
from gs.group.messages.add.smtp2gs.script import (
    get_token_from_config, get_relay_address_prefix_from_config,
    cleanup_lock, add_post_to_groupserver)
import gs.group.messages.add.smtp2gs.script as gsscript


class TestScript(TestCase):
    tokenValue = 'tokenValue'
    prefix = 'not-the-actual-prefix'

    def setUp(self):
        gsscript.Config.__init__ = MagicMock(return_value=None)
        gsscript.Config.set_schema = MagicMock()
        fauxConfig = {'token': self.tokenValue,
                      'relay-address-prefix': self.prefix}
        gsscript.Config.get = MagicMock(return_value=fauxConfig)
        gsscript.sys.exit = MagicMock()

        gsscript.lock = MagicMock()
        self.oldWeLocked = gsscript.weLocked

    def tearDown(self):
        gsscript.weLocked = self.oldWeLocked

    def test_get_token_from_config(self):
        'Test that we get the token from the config'
        r = get_token_from_config('default', 'gsconfig.ini')
        self.assertEqual(self.tokenValue, r)
        self.assertEqual(1, gsscript.Config.__init__.call_count)
        self.assertEqual(1, gsscript.Config.set_schema.call_count)
        self.assertEqual(1, gsscript.Config.get.call_count)
        args, kw_args = gsscript.Config.__init__.call_args
        self.assertEqual('default', args[0])
        self.assertEqual('gsconfig.ini', args[1])

    def test_get_token_from_config_missing(self):
        'Test that we raise an error when the token is missing'
        gsscript.Config.get = MagicMock(return_value={'token': None})
        with self.assertRaises(ValueError):
            get_token_from_config('default', 'gsconfig.ini')

    def test_get_relay_address_prefix_from_config(self):
        'Test that we get the relay-address prefix from the config'
        r = get_relay_address_prefix_from_config('default', 'gsconfig.ini')
        self.assertEqual(self.prefix, r)
        self.assertEqual(1, gsscript.Config.__init__.call_count)
        self.assertEqual(1, gsscript.Config.set_schema.call_count)
        self.assertEqual(1, gsscript.Config.get.call_count)
        args, kw_args = gsscript.Config.__init__.call_args
        self.assertEqual('default', args[0])
        self.assertEqual('gsconfig.ini', args[1])

    def test_get_relay_address_prefix_from_config_missing(self):
        'Test that we get "p-" when the prefix is missing'
        gsscript.Config.get = MagicMock(return_value={})
        r = get_relay_address_prefix_from_config('default', 'gsconfig.ini')
        self.assertEqual('p-', r)

    def test_cleanup_lock_unlock(self):
        'Test that cleanup_lock unlocks when it should'
        gsscript.weLocked = True
        cleanup_lock()
        self.assertEqual(1, gsscript.lock.release.call_count)

    def test_cleanup_lock_untouched(self):
        'Test that cleanup_lock leaves the lock locked when it should'
        gsscript.weLocked = False
        cleanup_lock()
        self.assertEqual(0, gsscript.lock.release.call_count)

    @patch('gs.group.messages.add.smtp2gs.script.sys')
    @patch('gs.group.messages.add.smtp2gs.script.'
           'get_group_info_from_address')
    @patch('gs.group.messages.add.smtp2gs.script.add_post')
    def test_no_relay_if_listid(self, m_add_post, m_ggi, m_sys):
        'Ensure we do not try and relay the message if the list ID is set'
        m = '''To: example-group@example.com
From: a.member@people.example.com
Subject: Violence

Good evening.

On Ethel the Frog tonight we look at violence: the violence of
British Gangland.'''
        add_post_to_groupserver(
            progName='gs.group.messages.add.smtp2gs.tests.script',
            url=b'http://groups.example.com',
            listId=b'example-group',
            emailMessage=m,
            token=b'fake-token',
            relayAddressPrefix='r-')

        # We have a list-ID, so get_group_info_from_address should not be
        # called
        self.assertEqual(0, m_ggi.call_count)
        m_add_post.assert_called_once_with(
            b'groups.example.com', False, b'example-group', m,
            b'fake-token')

    @patch('gs.group.messages.add.smtp2gs.script.sys')
    @patch('gs.group.messages.add.smtp2gs.script.'
           'get_group_info_from_address')
    @patch('gs.group.messages.add.smtp2gs.script.add_post')
    def test_orig_if_no_listid(self, m_add_post, m_ggi, m_sys):
        'Ensure we use the x-original-to if we lack a list-id'
        # The lack of the group address in any standard destination address
        # happens if BCC gets used.
        m = '''To: someone.else@others.example.com
From: a.member@people.example.com
Subject: Violence
X-Original-To: example-group@groups.example.com

Good evening.

On Ethel the Frog tonight we look at violence: the violence of
British Gangland.'''

        m_ggi.return_value = {'groupId': 'example-group'}

        add_post_to_groupserver(
            progName='gs.group.messages.add.smtp2gs.tests.script',
            url=b'http://groups.example.com',
            listId=None,
            emailMessage=m,
            token=b'fake-token',
            relayAddressPrefix='r-')

        # We have a list-ID, so get_group_info_from_address should not be
        # called
        m_ggi.assert_called_once_with(
            b'groups.example.com', False,
            'example-group@groups.example.com', b'fake-token')
        m_add_post.assert_called_once_with(
            b'groups.example.com', False, b'example-group', m,
            b'fake-token')

    @patch('gs.group.messages.add.smtp2gs.script.relay_email')
    @patch('gs.group.messages.add.smtp2gs.script.'
           'get_group_info_from_address')
    @patch('gs.group.messages.add.smtp2gs.script.add_post')
    def test_relay(self, m_add_post, m_ggi, m_relay_email):
        m = '''To: r-memberId@groups.example.com
From: a.member@people.example.com
Subject: Violence
X-Original-To: z-memberId@groups.example.com

Good evening.

On Ethel the Frog tonight we look at violence: the violence of
British Gangland.'''
        add_post_to_groupserver(
            progName='gs.group.messages.add.smtp2gs.tests.script',
            url=b'http://groups.example.com',
            listId=None,
            emailMessage=m,
            token=b'fake-token',
            relayAddressPrefix='z-')

        m_relay_email.assert_called_once_with(
            b'groups.example.com', False, m, b'fake-token')
