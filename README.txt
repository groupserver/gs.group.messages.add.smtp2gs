Introduction
============

This is the core code for adding a message to a `GroupServer`_ group. This
module supplies:

* The `smtp2gs`_ script, which allows the external mail-transfer agent to
  add the message to GroupServer.
* A page to `check if a group exists`_,
* A page to `add an email`_ to a group.

``smtp2gs``
===========

Usually a SMTP server (such as Postfix) will call ``smtp2gs is`` to add an
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


Check if a Group Exists
=======================

The code to check if a group exists [#exists]_ is a simple form,
``/gs-group-messages-add-group-exists.html``, that is designed to be called
from an external script. It takes two arguments:

#. The email address to check, and
#. The authentication token [#auth]_.

If the authentication token matches then a JSON object is returned. It has
the following values set:

``email``:
  The email address that was checked.

``groupId``:
  The ID of the group that was matched.

``siteId``:
  The ID of the site that the group belongs to.

``siteUrl``:
  The URL for the site that the group belongs. This is used to `add an
  email`_.

If there is no match then ``groupId``, ``siteId``, and ``siteUrl`` will be
``null``.

Add an Email
============

The code to add an email message to a group [#add]_ is a simple form,
``/gs-group-messages-add-email.html``. It takes an email message (including
its header) and a authentication token [#auth]_. It then passes the email
message on to the correct mailing-list, which it determines from the
``x-original-to`` header.

The Adder
---------

The ``gs.group.messages.add.adder.Adder`` class adds the message to the
group::
  
  Adder(context, request, siteId, groupId)

(The ``request`` is needed because of `a hack`_.) Multiple messages can be
added with a single Adder instance by calling the `add`_ method.

``add``
~~~~~~~

The ``Adder.add`` method takes a message as a single argument, and adds the
message to the list. It returns the identifier of the post that has just
been added.

A Hack
~~~~~~

The code to add a message to a group is built around a hack, where it adds
the message as an element of the ``REQUEST.form``. The request is needed
for the can-post [#canpost]_ to create the correct error-message for the
email-notification that is sent if the person who sent the message cannot
post.

What *should* happen is the job of sending the notification should be moved
from the mailing list. Instead, the list should throw an exception if the
user cannot post, and the *form* should catch it and send out the
notification.

``add_a_post``
--------------

The utility function ``gs.group.messages.add.add_a_post`` adds a post to a
group.

Synopsis
~~~~~~~~

::

   add_a_post(groupId, siteId, replyToId, topic, message, tags, email, 
              uploadedFiles, context, request)

Arguments
~~~~~~~~~

``groupId``:
  The ID of the group to add the post to.

``siteId``:
  The ID of the site to add the post to.

``replyToId``:
  The ID of the post that the person is replying to. It may be none.

``topic``:
  The topic (subject) to add the post to.

``message``:
  The message to add to the topic.

``tags``:
  Deprecated.

``email``:
  The ``From`` email address.

``uploadedFiles``:
  A list of files (attachments) that have been added to the post.

``context``:
  The context.

``request``:
  A request.

Returns
~~~~~~~

The ID of the post that has been added.

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#exists] See `Feature 3537 <https://redmine.iopen.net/issues/3537>`_
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. [#add] See `Feature 3538 <https://redmine.iopen.net/issues/3538>`_
.. [#canpost] See ``gs.group.member.canpost``
      <https://source.iopen.net/groupserver/gs.group.member.canpost/summary>
.. _GroupServer: http://groupserver.org/
