# coding=utf-8
from cStringIO import StringIO
from zope.cachedescriptors.property import Lazy
from zope.publisher.base import TestRequest
from Products.XWFMailingListManager.utils import MAIL_PARAMETER_NAME

class Adder(object):
    def __init__(self, context, siteId, groupId):
        assert self.context, 'No context'
        self.context = context
        assert siteId, 'No siteId'
        self.siteId = siteId
        assert groupId, 'No groupId'
        self.groupId = groupId
    
    @Lazy
    def list(self):
        listManager = self.context.ListManager
        assert hasattr(listManager, self.groupId),\
            'No such list "%s"' % self.groupId
        retval = listManager.get_list(self.groupId)
        assert retval
        return retval

    def add(self, message):
        # TODO: audit
        path = '/ListManager/%s/manage_mailboxer' % self.groupId
        r = TestRequest(path)
        r[MAIL_PARAMETER_NAME] = message
        self.list.manage_mailboxer(r)
