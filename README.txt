Introduction
============

This is the core code for adding a message to a `GroupServer`_ group. This
module supplies:

* A page to determine if a `group exists`_,
* A page to add an email to a group [#add]_, and
* An entry-point, so the external mail-transfer agent can add the message
  easily [#entryPoint]_

Group Exists
============

The code to check if a group exists [#exists]_ is a simple form,
``/gs-group-messages-add-group-exists.html``, that is designed to be called
from an external script. It takes two arguments:

#. The email address to check
#. The authentication token (see ``gs.auth.token``).

If the authentication token matches then a JSON object is returned. It has
the following values set:

``email``:
  The email address that was checked.

``groupId``:
  The ID of the group that was matched.

``siteId``:
  The ID of the site that the group belongs to.

If there is no match then both ``groupId`` and ``siteId`` will be ``null``.

.. [#exists] See `Feature 3537 <https://redmine.iopen.net/issues/3537>`_
.. [#add] See `Feature 3538 <https://redmine.iopen.net/issues/3538>`_
.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. _GroupServer: http://groupserver.org/
