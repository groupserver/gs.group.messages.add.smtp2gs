# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.publisher.base import TestRequest
from Products.XWFMailingListManager.utils import MAIL_PARAMETER_NAME

class Adder(object):
    def __init__(self, context, request, siteId, groupId):
        assert context, 'No context'
        self.context = context
        assert request, 'No request'
        self.request = request
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
        r = self.request.clone()
        r.form[MAIL_PARAMETER_NAME] = message
        retval = self.list.manage_mailboxer(r)
        assert retval
        assert type(retval) in (unicode, str)
        return retval
