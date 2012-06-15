# coding=utf-8
from zope.interface.interface import Interface
from zope.schema import ASCIILine
# TODO: AuthToken

class IGSGroupExists(Interface):
    email = ASCIILine(title=u'Email Address',
                      description=u'The email address to check',
                      required=True)
    # TODO: Create a base email-address type
