Changelog
=========

3.0.1 (2015-03-30)
------------------

* Avoiding the relay code if the list-identifier is specified,
  `thanks to Piers`_
* Dropping `gs.profile.email.relay`_ from the product
  dependencies: it does rely on it, but for the page rather than
  for the code
* Adding more unit tests

.. _`thanks to Piers`:
   http://groupserver.org/r/post/7KTJlimsOi1l8sKLiPsD3P
.. _gs.profile.email.relay:
   https://github.com/groupserver/gs.profile.email.relay

3.0.0 (2015-03-17)
------------------

* Relaying on email messages to group members, closing `Feature
  4106`_

.. _Feature 4106: https://redmine.iopen.net/issues/4106

2.1.3 (2015-02-12)
------------------

* Adding the documentation to `Read the Docs`_

.. _Read the Docs: 

2.1.2 (2014-10-24)
------------------

* Switching to GitHub_ as the primary code repository, naming the
  reStructuredText files as such.

.. _GitHub: https://github.com/groupserver/gs.group.messages.add.smtp2gs

2.1.1 (2014-06-18)
------------------

* Fixing a race-condition, with thanks to Iris.

2.1.0 (2014-05-05)
------------------

* Added Python 3 support.
* Added unit tests.
* Handle the absence of an ``x-original-to`` header if the list
  identifier is provided.

2.0.2 (2014-04-09)
------------------

* Fixing an error with the arguments to the script.

2.0.1 (2014-02-06)
------------------

* Switching to Unicode literals.

2.0.0 (2013-08-27)
------------------

* Added SSL handling, `thanks to Tom.
  <http://groupserver.org/r/pos t/5tGuPa4ul9W9CN8dkVaZ2>`_
* Updating the product metadata.

1.0.1 (2012-11-30)
------------------

* PEP-8 and Python 2.6 cleanup

1.0.0 (2012-08-01)
------------------

* Initial version, based on a script in
  ``XWFMailingListManager``.

..  LocalWords:  Changelog GitHub
