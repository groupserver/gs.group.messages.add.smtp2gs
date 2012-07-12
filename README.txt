Introduction
============

This is the core code for adding a message to a `GroupServer`_ group. This
module supplies:

* A page to `check if a group exists`_,
* A page to `add an email`_ to a group, and
* An entry-point, so the external mail-transfer agent can add the message
  easily [#entryPoint]_

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

Multiple messages can be added with a single instance. The ``request`` is
needed because of `a hack`_.

The ``Adder.add`` method takes a message as a single argument, and adds the
message to the list.

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

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#exists] See `Feature 3537 <https://redmine.iopen.net/issues/3537>`_
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. [#add] See `Feature 3538 <https://redmine.iopen.net/issues/3538>`_
.. [#canpost] See ``gs.group.member.canpost``
      <https://source.iopen.net/groupserver/gs.group.member.canpost/summary>
.. _GroupServer: http://groupserver.org/
