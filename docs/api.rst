:mod:`gs.group.messages.add.smtp2gs` Internals
==============================================

.. currentmodule:: gs.group.messages.add.smtp2gs

The :mod:`gs.group.messages.add.smtp2gs` does not have a public
API, other than what is provided by the script itself. However,
the internals are documented below.

The script
----------

The ``smtp2gs`` script is provided by the module
:mod:`.script`. The :func:`main` function takes the name of the
default configuration file a single argument, which is normally
supplied by ``buildout`` when it generates the ``smtp2gs`` script
from the entry point.

The script parses the command-line arguments, and calls two
further functions:

:func:`.servercomms.get_group_info_from_address`:
  This calls the page ``/gs-group-messages-add-group-exists.html`` to check
  if the group exists, and to get some information about the group.

:func:`.servercomms.add_post`:
  This calls the page ``/gs-group-messages-add-email.html`` to actually add
  the post.

Both pages are provided by the ``gs.group.messages.add.base``
product [#add]_; the data is sent by the
``gs.form.post_multipart`` function [#form]_, with
``gs.auth.token`` [#auth]_ providing authentication (see
:doc:`config`).

.. automodule:: gs.group.messages.add.smtp2gs.script
   :members: main, add_post_to_groupserver

Exit values
-----------

.. automodule:: gs.group.messages.add.smtp2gs.errorvals
   :members: EX_OK, EX_USAGE, EX_DATAERR, EX_NOUSER, EX_PROTOCOL, EX_TEMPFAIL,
             EX_CONFIG

XVERP
-----
.. automodule:: gs.group.messages.add.smtp2gs.xverp
   :members: is_an_xverp_bounce, handle_bounce

Locking
-------

.. automodule:: gs.group.messages.add.smtp2gs.locker
   :members: get_lock, LOCK_NAME, MAX_LOCK_TIMEOUT, BREAK_LOCK_AGE

Server communications
---------------------

.. automodule:: gs.group.messages.add.smtp2gs.servercomms
   :members:

.. [#add] See ``gs.group.messages.add.base`` 
          <https://github.com/groupserver/gs.group.messages.add.base>
.. [#form] See ``gs.form`` 
           <https://github.com/groupserver/gs.form>
.. [#auth] See ``gs.auth.token`` 
           <https://github.com/groupserver/gs.auth.token>
