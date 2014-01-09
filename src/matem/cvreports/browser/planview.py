# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from matem.cvreports import cvreportsMessageFactory as _

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import datetime

class IReportView(Interface):
    """
    Report view interface
    """

    def usuarios():
        """ regresa investigadores activos"""

    def rango():
        """ de alguna manera regresara el año al que se refieren los planes de trabajo """


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

    def usuarios(self):
        query = {}
        query['portal_type'] = 'FSDPerson'
        brains = self.portal_catalog.searchResults(query)
        gente = []
        for brain in brains:
            persona = brain.getObject()
            esta_activo = getToolByName(self.context, 'portal_workflow').getInfoFor(persona, 'review_state') == 'active'
            clasificaciones = persona.getClassificationNames()
            if 'Investigadores' in clasificaciones and esta_activo:
                gente.append(persona)
        g = sorted(gente, key=lambda person: person.lastName)
        return g

    def rango(self):
        return ('2007')
