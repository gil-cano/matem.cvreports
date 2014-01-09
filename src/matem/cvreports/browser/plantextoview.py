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

    def proyectos():
        """ Obtiene todos los proyectos que pertenezcan al investigador,
        vigentes en el rango indicado """

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

    def proyectosEnRango(self):
        """ regresa los proyectos que se encuentran entre el rango de fechas especificado """
        year = self.request.get('year')
        year = int(year)
        query = {}
        query['portal_type'] = 'CVProject'

        desde = datetime.date(year, 01, 01)
        hasta =  datetime.date(year, 12, 31)
        query['fecha_termino'] = {
            'query' : [hasta,],
            'range' : 'min'}
        query['fecha_inicio'] = {
            'query' : [desde,],
            'range' : 'max'}
        brains = self.portal_catalog.searchResults(query)
        proyectos = [brain.getObject() for brain in brains]

        return proyectos

    def llenaBasicos(self, probableProyecto):
        """ mete a resultado los valores 'generales' del proyecto en cuestion """
        resultado = {'invest' : self.request.get('nombre')}
        resultado['participacion'] = 'None'
        resultado['titulo'] =  probableProyecto.Title()
        resultado['proyectoUrl'] = probableProyecto.absolute_url()
        resultado['colaboradoresInternos'] = probableProyecto.getInternalCollaborators()
#            resultado['colaboradoresExternos'] = probableProyecto.getExternalCollaborators()
        return resultado

    def proyectos(self):
        """ Primero hago el query restringiendo a contenido de tipo Proyecto, vigentes.
        Con el for obtendré solo los proyectos en los que el investigador
        sea responsable, colaborador o corresponsable """
        query = {}
        Investigadores = []
        if self.request.get('id') == 'todos':
            query['portal_type'] = 'FSDClassification'
            query['id'] = 'investigadores'
            brains = self.portal_catalog.searchResults(query)
            Investigadores = brains[0].getObject().getPeople()
        else:
            query['portal_type'] = 'FSDPerson'
            query['id'] = self.request.get('id')
            brains = self.portal_catalog.searchResults(query)
            Investigadores.append(brains[0].getObject())

#         Investigadores = [brain.getPeople() for brain in brains]
        proyectos = self.proyectosEnRango()
        diccionarioFinal = {}

        """ resultado será una lista de diccionarios en donde cada diccionario es de la forma
        {'invest': nombre, 'titulo': Title, 'proyecto_url': absolute_url, 'patrocinador': sponsor, 'participacion': (responsable | corresponsable | colaborador),
        'lineas':[{'item1':textolinea1, 'item2':textolinea2,...}], 'objetivo': texto, 'tipo':inves|divulg,
        'colaboradores': [colabora1, colabora2,...] """
        for investigador in Investigadores:
            diccionarioInvestigador = {}
            listaProyectos = []
            idInvestigador = investigador.id
            for probableProyecto in proyectos:
                resultado = self.llenaBasicos(probableProyecto)
                esResponsable = esCorresponsable = esColaborador = False

                if (probableProyecto.getInternalResponsible() != None):
                    if (probableProyecto.getInternalResponsible().id == idInvestigador):
                        esResponsable = True
                        resultado['participacion'] = 'responsable'
                if (probableProyecto.getInternalCorresponsible() != None):
                    if (probableProyecto.getInternalCorresponsible().id == idInvestigador):
                        esCorresponsable = True
                        resultado['participacion'] = 'corresponsable'
                if (probableProyecto.getInternalCollaborators() != None):
                    for persona in resultado['colaboradoresInternos']:
                        if persona.id == idInvestigador:
                            esColaborador = True
                            resultado['colaboradoresInternos'] = resultado['colaboradoresInternos'].remove(persona)
                            resultado['participacion'] = 'colaborador'

                if esResponsable or esCorresponsable or esColaborador:
                    resultado['tipo'] = probableProyecto.getProjectType()
                    resultado['tieneLineas'] = len(probableProyecto.getResearchRef()) != 0
                    resultado['lineas'] = ()
                    resultado['lineas'] = probableProyecto.getResearchRef()
                    if esColaborador:
                        if resultado['colaboradoresInternos'] != None:
                            resultado['tieneColaboradoresInternos'] = len(resultado['colaboradoresInternos']) != 0
                        else:
                            resultado['tieneColaboradoresInternos'] = False
                    else:
                        resultado['tieneColaboradoresInternos'] = len(resultado['colaboradoresInternos']) != 0
                    if (probableProyecto.getExternalCollaborators() != None) and (len(probableProyecto.getExternalCollaborators()) != 0):
                        resultado['tieneColaboradoresExternos'] = True
                        resultado['colaboradoresExternos'] = probableProyecto.getExternalCollaborators()
                    else:
                        resultado['tieneColaboradoresExternos'] = False
                    resultado['tienePatrocinador'] = probableProyecto.getSponsor() != ''
                    resultado['patrocinador'] = probableProyecto.getSponsor()
                    resultado['tieneObjetivo'] = probableProyecto.getAim() != ''
                    resultado['objetivo'] = probableProyecto.getAim()
                    resultado['tieneColaboradores'] = resultado['tieneColaboradoresInternos'] or resultado['tieneColaboradoresExternos']
                    listaProyectos.append(resultado)
            if len(listaProyectos) != 0:
#                 diccionarioFinal[idInvestigador] = listaProyectos
                diccionarioInvestigador['nombreInvestigador'] = investigador.Title()
                diccionarioInvestigador['proyectos'] = listaProyectos
                diccionarioFinal[idInvestigador] = diccionarioInvestigador
        return diccionarioFinal


