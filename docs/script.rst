:program:`smtp2gs`
==================

.. program:: smtp2gs

Synopsis
--------

   :program:`smtp2gs` [:option:`-h`] [:option:`-m` <MAXSIZE>] [:option:`-l` <LISTID>] [:option:`-f` <FILE>] [:option:`-c` <CONFIG>] [:option:`-i` <INSTANCE>] :option:`url`

Description
-----------

:program:`smtp2gs` to adds an email message to a GroupServer
group. It is usually called by an SMTP server (such as
:command:`postfix`).

Positional Arguments
--------------------

.. option:: url

  The URL for the GroupServer site.

Optional Arguments
------------------

.. option:: -h, --help

  Show a help message and exit

.. option:: -m <MAXSIZE>, --max-size <MAXSIZE>

  The maximum size of the post that will be accepted, in
  mebibytes (default 200MiB).

.. option:: -l <LISTID>, --list <LISTID>

  The list to send the message to. By default it is extracted
  from the :mailheader:`x-original-to` header.

.. option:: -f <FILE>, --file <FILE>

  The name of the file that contains the message. If omitted (or
  ``-``) standard-input will be read.

.. option:: -c <CONFIG>, --config <CONFIG>

  The name of the GroupServer :doc:`config` (default
  :file:`{INSTANCE_HOME}/etc/gsconfig.ini`) that contains the
  token that will be used to authenticate the script when it
  tries to add the email to the site.

.. option:: -i <INSTANCE>, --instance <INSTANCE>

  The identifier of the GroupServer instance configuration to use
  (default ``default``).

Returns
-------

:program:`smtp2gs` returns ``0`` on success, or a non-zero value
on an error (following the convention specified in
:file:`/usr/include/sysexits.h`). In addition the error message
that is written to ``stderr`` starts with the enhanced mail
system status code :rfc:`3463`. These include `transient errors`_
and `permanent errors`_.

Transient Errors
~~~~~~~~~~~~~~~~

Any errors that can be solved by changing the configuration
(either of :command:`postfix` or the :doc:`config`) are marked as
*transient* (with a :samp:`4.{x}.{x}` status code).

======  ===================================  ==================================
 Code    Note                                 Fix
======  ===================================  ==================================
 4.3.5   Error with the configuration file.   Correct the :doc:`config`.
 4.4.4   Error connecting to URL.             Check that the server is running,
                                              or alter the URL that is used to
                                              call :program:`smtp2gs`.
 4.4.5   The system is too busy.              Wait.
 4.5.0   Could not decode the data            *Usually* this is caused by an
         returned by the server.              invalid token in the
                                              :doc:`config`.
                                              Fix the token in the file.
 4.5.2   No host in the URL.                  Alter the URL that is used in
                                              the call to :program:`smtp2gs` so
                                              it has a host-name.
======  ===================================  ==================================


Permanent Errors
~~~~~~~~~~~~~~~~

The five *permanent* errors are listed below.

======  ======================================================================
 Code    Note
======  ======================================================================
 5.1.1   There is no such group to send the message to.
 5.1.3   No :mailheader:`x-original-to` header in the email message.
 5.3.0   The file containing the email was empty.
 5.3.4   Email message too large.
 5.5.0   Error communicating with the server (either while looking up the
         group information or adding the message).
======  ======================================================================

Examples
--------

Adding a post to a group in the general case, where the email is
read of standard input:

.. code-block:: console

  $ smtp2gs http://groups.example.com

Over-riding the :mailheader:`x-original-to` header. This allows
posts to an old email address to be sent to a new group.

.. code-block:: console

  $ smtp2gs --list newGroupId http://groups.example.com

Testing, by reading a file from :file:`/tmp`

.. code-block:: console

  $ smtp2gs --file /tmp/test.mbox http://groups.example.com

Setting the maximum size of messages posted to a group to 1MiB

.. code-block:: console

  $ smtp2gs --max-size 1 http://groups.example.com

Using the token for a specific GroupServer instance called
``production``

.. code-block:: console

  $ smtp2gs --instance production http://groups.example.com
