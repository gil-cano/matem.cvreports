# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from matem.cvreports import cvreportsMessageFactory as _

RESULTADO = {'header' : ['Titulo', 'Autores', 'Investigador','Capítulo','Editor','Editorial','País','Líneas de Investigación','Fecha de publicación','Notas'],
'data' : [[('fsd/merino/cv/cvbookchapterfolder/capituloreference.2008-12-05.1729645803', '1 Structural Analysis of Complex Networks'),'Joanna Ellis-Monaghan and Criel Merino','Criel Merino López','Graph polynomials and their applications I: the Tutte polynomial','Matthias Dehmer','Birkhäuser','Germany','05-xx Combinatoria','----/----/----','Aceptado pero todavía no publicado'],[('fsd/merino/cv/cvbookchapterfolder/capituloreference.2008-12-05.1729645803', '2. Structural Analysis of Complex Networks'),'Joanna Ellis-Monaghan and Criel Merino','Criel Merino López','Graph polynomials and their applications I: the Tutte polynomial','Matthias Dehmer','Birkhäuser','Germany','05-xx Combinatoria','----/----/----','Aceptado pero todavía no publicado']] }

class IReportView(Interface):
    """
    Report view interface
    """

    def test():
        """ test method """

    def form():
        """ form method """

    def ordena():
        """ sort method for RESULTADO """


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
#         dummy = self.context.getCvcontent()
#         brains = self.portal_catalog(portal_type=dummy)
#         data = []
#         for brain in brains:
#             dic = []
#             dic.append(brain['Title'])
#             dic.append(('','','','','',''))
#             data.append(dic)
#         RESULTADO['data'] = data

        return RESULTADO

    def ordena(self):
        """
        recibe un diccionario con dos listas y lo regresa ordenada alfabeticamente de acuerdo
        a la primera lista, que suponemos tiene los headers; la segunda es una lista de lista
        con los datos.
        """
        lista = self.form()
        encab_orig = lista['header']
        encab_ord = encab_orig[:]
        encab_ord.sort()
        datos = []
        renglones = lista['data']
        for renglon in renglones:
           reng_ord =[]
           i = 0
           for columna in encab_ord:
               j = encab_orig.index(columna)
               reng_ord.insert (i, renglon[j])
               i = i + 1
           datos.append(reng_ord)

        resultado = {'header':encab_ord, 'data':datos}

        return resultado

    def tabular(self):
        """
        returns a tabular representation
        """
        dummy = _(u'a tabular view')

        return {'dummy': dummy}

