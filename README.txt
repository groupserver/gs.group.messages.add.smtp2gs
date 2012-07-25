Introduction
============

This is the code for the `smtp2gs`_ script, which allows the external
mail-transfer agent to add the message to `GroupServer`_.  The
`configuration file`_ contains some information that allows the script to
authenticate with the site.

``smtp2gs``
===========

Usually a SMTP server (such as Postfix) will call ``smtp2gs`` to add an
email message to a GroupServer group. It is defined as an entry point
[#entryPoint]_ to this module.

Usage
-----

::

   smtp2gs [-h] [-m MAXSIZE] [-l LISTID] [-f FILE] [-c CONFIG] [-i INSTANCE] url

Positional Arguments
~~~~~~~~~~~~~~~~~~~~

``url``:
  The URL for the GroupServer site.

Optional Arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``:
  Show a help message and exit

``-m MAXSIZE``, ``--max-size MAXSIZE``:
  The maximum size of the post that will be accepted, in mebibytes (default 
  200MiB).

``-l LISTID``, ``--list LISTID``:
  The list to send the message to. By default it is extracted from the 
  ``x-original-to`` header.

``-f FILE``, ``--file FILE``:
  The name of the file that contains the message. If omitted (or "-") 
  standard-input will be read.

``-c CONFIG``, ``--config CONFIG``:
  The name of the GroupServer `configuration file`_ (default
  "$INSTANCE_HOME/etc/gsconfig.ini") that contains the token that will be
  used to authenticate the script when it tries to add the email to the
  site.

``-i INSTANCE``, ``--instance INSTANCE``:
  The identifier of the GroupServer instance configuration to use (default
  "default").

Examples
~~~~~~~~

Adding a post to a group in the general case, where the email is read of
standard input::

  smtp2gs http://url.of.your.site

Over-riding the ``x-original-to`` header. This allows posts to an old email
address to be sent to a new group.::

  smtp2gs --list newGroupId http://url.of.your.site

Testing, by reading a file from ``/tmp``::

  smtp2gs --file /tmp/test.mbox http://url.of.your.site

Setting the maximum size of messages posted to a group to 1MiB::

  smtp2gs --max-size 1 http://url.of.your.site

Using the token for a specific GroupServer instance called ``production``::

  smtp2gs --instance production http://url.of.your.site

The Code
--------

The ``smtp2gs`` script is provided by the module
``gs.group.messages.add.smtp2gs.script``. The ``main`` function takes the
name of the default configuration file a single argument, which is normally
supplied by ``buildout`` when it generates the ``smtp2gs`` script from the
entry point.

The script parses the command-line arguments, and calls two further functions:

``gs.group.messages.add.smtp2gs.servercomms.get_group_info_from_address``:
  This calls the page ``/gs-group-messages-add-group-exists.html`` to check
  if the group exists, and to get some information about the group.

``gs.group.messages.add.smtp2gs.servercomms.add_post``:
  This calls the page ``/gs-group-messages-add-email.html`` to actually add
  the post.

Both pages are provided by the ``gs.group.messages.add.base`` module
[#add]_; the data is sent by the ``gs.form.post_multipart`` function
[#form]_, with ``gs.auth.token`` [#auth]_ providing authentication (see the
section `Configuration File`_ below).

Configuration File
==================

The configuration for the ``smtp2gs`` script is handled by the
``gs.config`` module [#config]_. It is entirely concerned with token
authentication [#auth]_. To authenticate script needs to pass a token to
the web pages that are used to add a post [#add]_. The pages compare the
token that was passed in to one that is stored in the database. If they
match the script is allowed to post.

Examples
--------

Below is the configuration of the token for the GroupServer instance
``default``::

  [webservice-default]
  token = theValueOfTheToken

A more complex system, which has separate ``testing`` and ``production``
environments::

  [config-testing]
  ...
  webservice = testing

  [config-production]
  ...
  webservice = production

  [webservice-testing]
  token = theValueOfTheTokenForTesting

  [webservice-production]
  token = theValueOfTheTokenForProduction

The token-configuration for two separate sites (accessed through different
URLs) that are supported by the same database::

  [config-firstSite]
  ...
  webservice = default

  [config-secondSite]
  ...
  webservice = default

  [webservice-default]
  token = theValueOfTheDefaultToken

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#add] See ``gs.group.messages.add.base`` 
            <https://source.iopen.net/groupserver/gs.group.messages.add.base/summary>
.. [#form] See ``gs.form`` 
            <https://source.iopen.net/groupserver/gs.form/summary>
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. [#config] See ``gs.config`` 
            <https://source.iopen.net/groupserver/gs.config/summary>
.. _GroupServer: http://groupserver.org/

..  LocalWords:  CONFIG config
