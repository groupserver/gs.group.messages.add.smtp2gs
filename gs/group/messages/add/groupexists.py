# coding=utf-8
import json
from operator import or_
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from gs.content.form.form import SiteForm
from interfaces import IGSGroupExists

class GroupExists(SiteForm):
    label = u'Check if a group exists'
    pageTemplateFileName = 'browser/templates/groupexists.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSGroupExists, render_context=False)
    
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)

    @Lazy
    def mailingListManager(self):
        assert self.context
        retval = self.context.ListManager
        assert retval
        return retval

    def get_group_id(self, emailAddr):
        try:
            l = self.mailingListManager.get_listFromMailto(emailAddr)
        except AttributeError, ae:
            retval = None
        else:
            retval = l.getId()
        return retval

    def get_site_id(self, emailAddr):
        try:
            l = self.mailingListManager.get_listFromMailto(emailAddr)
        except AttributeError, ae:
            retval = None
        else:
            retval = l.getProperty('siteId')
        return retval

    @form.action(label=u'Check', failure='handle_check_action_failure')
    def handle_check(self, action, data):
        emailAddr = data['email']
        d = {
            'email':   emailAddr, 
            'groupId': self.get_group_id(emailAddr),
            'siteId':  self.get_site_id(emailAddr),
            }
        self.status = u'Done'
        retval = json.dumps(d)
        return retval

    def handle_check_action_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

