"""Definition of the CV Report content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from matem.cvreports import cvreportsMessageFactory as _
from matem.cvreports.interfaces import ICVReport
from matem.cvreports.config import PROJECTNAME
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

CVReportSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'cvcontent',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Seleccione el reporte que desea obtener"),
            description=_(u""),
            format="select",
        ),
        required=True,
        vocabulary_factory="matem.cvreports.vocabularies.cvcontenttypes"
    ),

    atapi.ReferenceField('rutaReportes',
        widget=ReferenceBrowserWidget(
            label=_(u"Carpeta donde se encuentran los reportes"),
            description=_(u""),
            allow_search=False,
            startup_directory='acerca-de/estructura-interna/secretaria-academica/informes/investigadores',
            show_path=True,
            force_close_on_insert=True,
        ),
        relationship="informes",
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

CVReportSchema['title'].storage = atapi.AnnotationStorage()
CVReportSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CVReportSchema, moveDiscussion=False)


class CVReport(base.ATCTContent):
    """reporte de algun contenido del cv"""
    implements(ICVReport)

    meta_type = "CV Report"
    schema = CVReportSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    cvcontent = atapi.ATFieldProperty('cvcontent')


atapi.registerType(CVReport, PROJECTNAME)
