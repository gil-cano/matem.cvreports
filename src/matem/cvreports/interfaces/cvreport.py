# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from matem.cvreports import cvreportsMessageFactory as _

class ICVReport(Interface):
    """reporte de algun contenido del cv"""

    # -*- schema definition goes here -*-
    cvcontent = schema.TextLine(
        title=_(u"Seleccione el reporte que desea obtener"),
        required=True,
        description=_(u"Field description"),
    )

