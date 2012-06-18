# coding=utf-8
from zope.interface.interface import Interface
from zope.schema import ASCIILine
from gs.auth.token import AuthToken

class IGSGroupExists(Interface):
    # TODO: Create a base email-address type
    email = ASCIILine(title=u'Email Address',
                      description=u'The email address to check',
                      required=True)
    token = AuthToken(title=u'Token',
                      description=u'The authentication token',
                      required=True)
