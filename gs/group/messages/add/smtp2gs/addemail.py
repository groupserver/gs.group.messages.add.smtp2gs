# coding=utf-8
from email.parser import Parser
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from adder import Adder
from base import ListInfoForm
from interfaces import IGSAddEmail

class AddEmail(ListInfoForm):
    label = u'Add an email'
    pageTemplateFileName = 'browser/templates/addemail.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSAddEmail, render_context=False)
    
    def __init__(self, context, request):
        ListInfoForm.__init__(self, context, request)

    def addr_from_email(self, emailMessage):
        parser = Parser()
        msgHdrs = parser.parsestr(emailMessage, headersonly=True)
        # A special header that is added by Postfix.
        retval = msgHdrs['x-original-to'] 
        assert retval, 'No x-original-to address'
        return retval

    @form.action(label=u'Add', failure='handle_add_action_failure')
    def handle_add(self, action, data):
        msg = data['emailMessage'].encode('utf-8')
        toAddr = self.addr_from_email(msg)
        adder = Adder(self.context, self.request,
                      self.get_site_id(toAddr), self.get_group_id(toAddr))
        adder.add(msg)
        self.status = u'Done'

    def handle_add_action_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode
