Configuration file
==================

The configuration for the ``smtp2gs`` script is handled by the
``gs.config`` module [#config]_. It is entirely concerned with
token authentication [#auth]_. To authenticate script needs to
pass a token to the web pages that are used to add a post
[#add]_. The pages compare the token that was passed in to one
that is stored in the database. If they match the script is
allowed to post.

Examples
--------

Below is the configuration of the token for the GroupServer instance
``default``:

.. code-block:: ini

  [webservice-default]
  token = theValueOfTheToken

A more complex system, which has separate ``testing`` and ``production``
environments:

.. code-block:: ini

  [config-testing]
  webservice = testing

  [config-production]
  webservice = production

  [webservice-testing]
  token = theValueOfTheTokenForTesting

  [webservice-production]
  token = theValueOfTheTokenForProduction

The token-configuration for two separate sites (accessed through different
URLs) that are supported by the same database:

.. code-block:: ini

  [config-firstSite]
  webservice = default

  [config-secondSite]
  webservice = default

  [webservice-default]
  token = theValueOfTheDefaultToken

.. [#add] See ``gs.group.messages.add.base``
          <https://github.com/groupserver/gs.group.messages.add.base>

.. [#auth] See ``gs.auth.token``
           <https://github.com/groupserver/gs.auth.token>

.. [#config] See ``gs.config``
             <https://github.com/groupserver/gs.config>
