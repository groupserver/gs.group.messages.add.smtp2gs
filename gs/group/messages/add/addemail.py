# coding=utf-8
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from interfaces import IGSAddEmail

class AddEmail(SiteForm):
    label = u'Add an email'
    pageTemplateFileName = 'browser/templates/addemail.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSAddEmail, render_context=False)
    
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)

    @form.action(label=u'Add', failure='handle_add_action_failure')
    def handle_add(self, action, data):
        self.status = u'Done'

    def handle_add_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

