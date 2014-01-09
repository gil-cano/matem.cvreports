# -*- coding: utf-8 -*-
from zope.interface import implements, Interface
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from matem.cvreports.browser.utils import listaAtributos
from matem.cvreports import cvreportsMessageFactory as _
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.ATCountryWidget.config import COUNTRIES
from DateTime.DateTime import DateTime

class IReportView(Interface):
    """
    Report view interface
    """

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
        """
        """
        content = self.context.getCvcontent()
        atypes = atapi.listTypes('UNAM.imateCVct')
        klasses = [atype['klass'] for atype in atypes]
        fields = []
        for klass in klasses:
            if klass.meta_type == content:
                o = klass('temp')
                schema = o.Schema()
                for field in schema.filterFields(isMetadata=0):
                    mydic = {'title': field.widget.label,
                    'fieldname': field.__name__}
                    mydic['vocabulary'] = ()
                    if field.__name__ == 'researchTopic':
                        factory = getUtility(IVocabularyFactory, 'imatem.person.specialties')
                        mydic['vocabulary'] = [(t.token, t.title) for t in factory(self)]
                    elif isinstance(field.vocabulary, DisplayList):
                        mydic['vocabulary'] = field.vocabulary.items()
                    fields.append(mydic)
                break
        return fields

    def personas(self):
        """
        """
        query = {}
        query['portal_type'] = 'FSDClassification'
        query['id'] = 'investigadores'
        query['review_state'] = 'active'
        brains = self.portal_catalog.searchResults(query)
        investigadores = brains[0].getObject().getSortedPeople()
        resultado = [('todos', 'Todos')]
        for investigador in investigadores:
            esta_activo = getToolByName(self.context, 'portal_workflow').getInfoFor(investigador, 'review_state') == 'active'
            if esta_activo:
                pareja = investigador.id, investigador.Title()
                resultado.append(pareja)
        return tuple(resultado)

    def years(self):
        """
        """
        return range(DateTime().year()+1, 1950, -1)
