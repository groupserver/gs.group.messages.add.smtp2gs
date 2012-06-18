# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.content.form.form import SiteForm

class ListInfoForm(SiteForm):
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
        self.map = {}

    @Lazy
    def mailingListManager(self):
        assert self.context
        retval = self.context.ListManager
        assert retval
        return retval

    def get_siteId_groupId_for_email(self, emailAddr):
        # TODO: making a nice big cache would be great
        if emailAddr not in self.map:
            l = self.mailingListManager.get_listFromMailto(emailAddr)
            self.map[emailAddr] = (l.getProperty('siteId'), l.getId())
        retval = self.map[emailAddr]
        assert len(retval) == 2
        return retval

    def get_site_id(self, emailAddr):
        retval = self.get_siteId_groupId_for_email(emailAddr)[0]
        return retval

    def get_group_id(self, emailAddr):
        retval = self.get_siteId_groupId_for_email(emailAddr)[1]
        return retval
