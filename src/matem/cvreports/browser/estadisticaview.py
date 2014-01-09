# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from matem.cvreports import cvreportsMessageFactory as _

RESULTADO = {'Total' : 15, 'Nacionales' : 4, 'Internacionales' : 11}

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

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def form(self):
        """
        returns a dic of {form field: posible value}
        """

        return RESULTADO

    def tabular(self):
        """
        returns a tabular representation
        """
        dummy = _(u'a tabular view')

        return {'dummy': dummy}

