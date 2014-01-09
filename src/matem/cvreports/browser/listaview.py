# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from matem.cvreports import cvreportsMessageFactory as _

ESTADISTICAS = {'CVBookChapter':('total', 'nacionales', 'internacionales',),
               }

RESULTADO = [{'Investigador': 'Criel Merino López' ,
'autores' : 'Joanna Ellis-Monaghan and Criel Merino',
'title' : 'Structural Analysis of Complex Networks',
'path' : 'fsd/merino/cv/cvbookchapterfolder/capituloreference.2008-12-05.1729645803',
'Capítulo' : 'Graph polynomials and their applications I: the Tutte polynomial',
'Editor' : 'Matthias Dehmer',
'Editorial' : 'Birkhäuser',
'País' : 'Germany',
'Líneas de Investigación' : '05-xx Combinatoria',
'Fecha de publicación' : '----/----/----',
'Notas' : 'Aceptado pero todavía no publicado'},
{'Investigador': 'Criel Merino López' ,
'autores' : 'Joanna Ellis-Monaghan and Criel Merino',
'title' : 'Structural Analysis of Complex Networks',
'Capítulo' : 'Graph polynomials and their applications I: the Tutte polynomial',
'Editor' : 'Matthias Dehmer',
'Editorial' : 'Birkhäuser',
'País' : 'Germany',
'Líneas de Investigación' : '05-xx Combinatoria',
'Fecha de publicación' : '----/----/----',
'Notas' : 'Aceptado pero todavía no publicado'}]

class IReportView(Interface):
    """
    Report view interface
    """

    def test():
        """ test method """

    def form():
        """ form method """

    def archivos():
        """ counting method """


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

    def archivos(self):
        """
        returns the number of elements that belongs to the list
        """

        return len (self.form())

    def tabular(self):
        """
        returns a tabular representation
        """
        dummy = _(u'a tabular view')

        return {'dummy': dummy}

