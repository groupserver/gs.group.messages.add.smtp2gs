# coding=utf-8
import json
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from base import ListInfoForm
from interfaces import IGSGroupExists

class GroupExists(ListInfoForm):
    label = u'Check if a group exists'
    pageTemplateFileName = 'browser/templates/groupexists.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSGroupExists, render_context=False)
    
    def __init__(self, context, request):
        ListInfoForm.__init__(self, context, request)

    def get_url_for_site(self, siteId):
        retval = None
        if siteId:
            s = getattr(self.context.Content, siteId)
            retval = createObject('groupserver.SiteInfo', s).url
        return retval

    @form.action(label=u'Check', failure='handle_check_action_failure')
    def handle_check(self, action, data):
        emailAddr = data['email']
        siteId = self.get_site_id(emailAddr)
        d = {
            'email':   emailAddr, 
            'siteId':  siteId,
            'groupId': self.get_group_id(emailAddr),
            'siteURL': self.get_url_for_site(siteId),
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

