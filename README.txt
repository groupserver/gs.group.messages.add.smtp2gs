Introduction
============

This is the code for the `smtp2gs`_ script, which allows the external
mail-transfer agent to add the message to `GroupServer`_. It is defined as
an entry point [#entryPoint]_.

``smtp2gs``
===========

Usually a SMTP server (such as Postfix) will call ``smtp2gs`` to add an
email message to a GroupServer group. It uses the pages provided by this
module to `check if a group exists`_, and to `add an email`_ to a group.

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

Configuration File
==================

Todo: Add configuration file handling.

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. _GroupServer: http://groupserver.org/
