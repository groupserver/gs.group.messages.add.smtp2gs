# coding=utf-8
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from interfaces import IGSGroupExists

class GroupExists(SiteForm):
    label = u'Check if a group exists'
    pageTemplateFileName = 'browser/templates/groupexists.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSGroupExists, render_context=False)
    
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
