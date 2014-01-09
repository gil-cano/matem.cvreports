from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from Products.Archetypes import atapi
from UNAM.imateCVct.interfaces.interfaces import ICVBaseActivity


class CVContentTypesVocabulary(object):
    """ Vocabulary factory for cv content types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        atypes = atapi.listTypes('UNAM.imateCVct')
        archetypes = [atype['klass'] for atype in atypes]
        archetypes.sort(key=lambda x: x.__name__)
        items = []
        portal_types = getToolByName(context, 'portal_types')
        for klass in archetypes:
            # TODO: CVTool rises an AttributeError
            # TODO: El vocablario reporta 4 cosas que no debe.
			# institucion, proyecto, reporte/informe, revista.
            try:
                o = klass('temp')
                if ICVBaseActivity.providedBy(o):
                    title = portal_types[klass.meta_type].title
                    items.append(SimpleTerm(klass.meta_type, title))
            except AttributeError:
                pass
        return SimpleVocabulary(items)

CVContentTypesVocabularyFactory = CVContentTypesVocabulary()
