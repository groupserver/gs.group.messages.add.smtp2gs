Introduction
============

This is the code for the `smtp2gs`_ script, which allows the external
mail-transfer agent to add the message to `GroupServer`_. It is defined as
an entry point [#entryPoint]_.

``smtp2gs``
===========

Usually a SMTP server (such as Postfix) will call ``smtp2gs`` to add an
email message to a GroupServer group. 

Usage
-----

::

   smtp2gs [-h] [-m MAXSIZE] [-l LISTID] [-f FILE] url

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

``-f FILE``, ``--file FILE``
  The name of the file that contains the message. If omitted (or "-") 
  standard-input will be read.

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


Configuration File
==================

Todo: Add configuration file handling.

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. _GroupServer: http://groupserver.org/
