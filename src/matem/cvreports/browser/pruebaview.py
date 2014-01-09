# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from matem.cvreports import cvreportsMessageFactory as _

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

class IReportView(Interface):
    """
    Report view interface
    """

    def test():
        """ test method """

    def form():
        """ form method """

class ReportView(BrowserView):
    """
    Report browser view
    """
    implements(IReportView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def form(self):
        v_factory = getUtility(IVocabularyFactory,
                               'imatem.person.specialties')
        svocabulary = v_factory(self)

        lineas = []
        for item in svocabulary.__iter__():
            lineas.append(item.title)
        return lineas

    def persona(self):
        pcatalog = getToolByName(self, 'portal_catalog')
        brains = pcatalog(portal_type='FSDPerson')
        people = [brain.getObject().Title for brain in brains]
        return people



