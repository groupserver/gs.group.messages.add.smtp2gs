:mod:`gs.group.messages.add.smtp2gs` Internals
==============================================

The :mod:`gs.group.messages.add.smtp2gs` does not have a public
API, other than what is provided by the script itself. However,
the internals are documented below.

The script
----------

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


