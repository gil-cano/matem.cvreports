# -*- coding: utf-8 -*-
from zope.interface import implements, Interface
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
from Products.DateFree.Date import DateFreeWidget
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from DateTime.DateTime import DateTime
from zope.component.hooks import getSite
from types import ListType


COLUMNS = {
    'CVArticle': ['title', 'publicationType', 'magazineRef', 'factor', 'othermagazine',
                  'number',
                  'colproceedingtitle', 'editor', 'authors', 'isnational',
                  'pages', 'isbn', 'volume', 'relatedProjects', 'sede'],
    'CVBook': ['booktype', 'title', 'authors', 'country', 'city', 'publisher',
                'edition', 'publication_date', 'pages', 'collection', 'serie',
                'volume', 'isbn', 'relatedProjects', 'sede'],
    'CVBookChapter': ['bookTitle', 'title', 'editor', 'authors', 'country',
                      'city', 'publisher', 'edition', 'publication_date',
                      'pages', 'collection', 'serie', 'volume', 'isbn',
                      'relatedProjects', 'sede'],
    'CVReport': ['title', 'authors', 'publication_date', 'pages', 'sede'],
    'CVRefereeing': ['creators', 'title', 'magazineRef', 'othermagazine',
                     'worksPerYear', 'sede'],
    'CVEventOrg': ['title', 'event_date', 'numberOfDays', 'institutions',
                   'nationalSpeakers', 'foreignSpeakers', 'assistants',
                   'eventType', 'instituteParticipation', 'creators', 'sede'],
    'CVConference': ['title', 'modality', 'meetingName', 'event_date',
                     'institutionCountry', 'city', 'assist', 'creators', 'sede'],
    'CVConferencePlus': ['title', 'meetingName', 'event_date',
                         'institutionCountry', 'city', 'creators', 'sede'],
    'CVAward': ['title', 'creators', 'institutionCountry', 'institution',
                'otherinstitution', 'isnational', 'sede'],
    'CVGuest': ['title', 'institutionCountry', 'institution',
                'otherinstitution', 'goalGuest', 'begin_date', 'end_date',
                'interchangeProgram', 'creators', 'sede'],
    'CVVisit': ['creators', 'institutionCountry', 'title', 'goalVisit',
                'begin_date', 'end_date', 'sede'],
    'CVCourse': ['level', 'courseName', 'coursetype', 'weekHours',
                 'numberOfHours', 'creators', 'institution',
                 'otherinstitution', 'sede'],
    'CVReview': ['organization', 'descriptionRev', 'articleTitle',
                 'event_date', 'creators', 'sede'],
    'CVThesis': ['title', 'thesisType', 'authorThesis', 'status_thesis',
                 'graduation_date', 'level', 'creators', 'institution',
                 'otherinstitution', 'sede'],
    'CVEvent': ['title', 'creators', 'audienceType', 'sede', 'where',
                'institutionCountry', 'country', 'conference'],
    'CVQualification': ['title', 'qualificationForm', 'grade', 'creators'],
    'CVStudieProgram': ['title', 'level', 'otherLevel', 'institution',
                        'begin_date', 'end_date', 'otherinstitution',
                        'description', 'creators'],
    'CVTeachingAid': ['title', 'aidType', 'description', 'begin_date',
                      'end_date', 'creators'],
    'CVReport': ['title', 'authors', 'reportType', 'pages',
                 'publication_date', 'creators'],
    'CVEditorialCom': ['title', 'description', 'commtype', 'begin_date', 'end_date', 'creators'],
}


class IReportView(Interface):
    """
    Report view interface
    """

    def formfields():
        """ form method """


class ReportView(BrowserView):
    """
    Report browser view
    """
    implements(IReportView)
    template = ViewPageTemplateFile('reportview.pt')
    tabularview = ViewPageTemplateFile('tabularview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.atype = self.context.cvcontent

    def __call__(self):
        form = self.request.form
        # make sure we had a proper form submit, not just GET request
        submitted = form.get('form.submitted', False)
        if not submitted:
            return self.template()

        self.request.set('disable_border', True)

        if form.get('form.button.tabular', None):
            return self.tabularview()

        # TODO: add more views
        return self.tabularview()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def formfields(self):
        """ generate a dinamic form from content schema.
        """
        content = self.context.getCvcontent()
        types = atapi.listTypes('UNAM.imateCVct')
        # klasses = [atype['klass'] for atype in types]
        klasses = [t['klass'] for t in types if t['klass'].meta_type == content]
        if not klasses:
            return []
        fields = []
        obj = klasses[0]('temp')
        schema = obj.Schema()
        for field in schema.filterFields(isMetadata=0):
            item = {'title': field.widget.label, 'type': 'text',
                    'index': field.getAccessor(obj).__name__, 'vocabulary': []}
            if isinstance(field.vocabulary, DisplayList):
                item['vocabulary'] = field.vocabulary.items()
                item['type'] = 'select'
                fields.append(item)
                continue
        return fields
            # if isinstance(field.widget, DateFreeWidget):
            #     item['type'] = 'datepicker'
            # if ((field.__name__ == 'authors') | \
            #     (field.__name__ == 'editors') | \
            #     (field.__name__ == 'internalCollaborators')):
            #     brain = self.portal_catalog(portal_type='FSDClassification',
            #         id='investigadores')
            #     # brain[0] must exist
            #     people = brain[0].getObject().getSortedPeople()
            #     item['vocabulary'] = [(p.id, p.Title()) for p in people]
            #     item['type'] = 'select'
            # elif field.__name__ == 'researchTopic':
            #     factory = getUtility(IVocabularyFactory,
            #                         'imatem.person.specialties')
            #     item['vocabulary'] = [(t.token, t.title) for t in factory(self)]
            #     item['type'] = 'select'
            # elif isinstance(field.vocabulary, DisplayList):
            #     item['vocabulary'] = field.vocabulary.items()
            #     item['type'] = 'select'
            # if field.searchable and field.__name__ != 'id':
            #     fields.append(item)
        # return fields

    def getColumnTitles(self):
        """returns a list of column titles"""
        brains = self.portal_catalog(portal_type=self.atype,
                                     sort_on='Date', sort_limit=8)
        if not self.atype in COLUMNS or not brains:
            return []
        obj = brains[0].getObject()
        labels = []
        for i in COLUMNS[self.atype]:
            if obj.getField(i):
                labels.append(obj.getField(i).widget.label)
            else:
                labels.append(i)
        return labels
        # return [obj.getField(i).widget.label for i in COLUMNS[self.atype]]

    def getMatchedItems(self):
        """ returns data as an iterable;
            each row is an (path, sequence of fields) tuple
        """
        form = self.request.form
        try:
            form.pop('form.submitted')
            form.pop('form.button.tabular')
        except:
            pass

        try:
            sede = form.pop('sede')
            if not isinstance(sede, ListType):
                sede = [sede]
        except:
            # if no sede selected all must be reported
            sede = ['df', 'matcuer', 'matjuriquilla']

        # esta no es la mejor manera de agregar el reporte de revistas
        # debemos encontrar una mejor manera de hacerlo
        # if self.type == 'CVMagazine':
        #     return self.getMagazineReport(form, sede)

        if not self.atype in COLUMNS:
            return []

        objs = self.matchContent(form, self.atype, sede)
        data = []
        vocabulary_fields = ['publicationType', 'isnational', 'modality', 'assist', 'eventType', 'instituteParticipation', 'thesisType', 'status_thesis', 'level', 'coursetype', 'booktype']
        for obj in objs:
            # try:
            #     magazine = obj.getMagazineRef().getIsIndexed()
            # except:
            #     magazine = obj.getOthermagazine()
            #     if magazine:
            #         magazine = True
            # row = [obj.Title(), magazine]
            row = []
            for i in COLUMNS[self.atype]:
                if i == 'authors':
                    row.append(obj.getAutorsString(obj.getField(i).get(obj)))
                elif i =='relatedProjects':
                    projects = [j.Title() for j in obj.getField(i).get(obj)]
                    row.append(', '.join(projects))
                elif i == 'publication_date':
                    row.append(obj.getField(i).get(obj).get('Year', None))
                elif i == 'creators':
                    ids = [j for j in obj.getField(i).get(obj)]
                    brains = self.portal_catalog(portal_type='FSDPerson', id=ids)
                    names = [j.Title for j in brains]
                    row.append(', '.join(names))
                elif i == 'magazineRef':
                    reference = ''
                    if obj.getField(i).get(obj):
                        reference = obj.getField(i).get(obj).Title()
                    row.append(reference)
                elif i == 'factor':
                    # debo mejorsr esta manera de recobrar el factor y que
                    # busque por año, un metodo en revista que responda esto.
                    factor = ''
                    if obj.getField('magazineRef').get(obj):
                        mag = obj.getField('magazineRef').get(obj)
                        if mag.getField('impactFactor').get(mag):
                            factor = mag.getField('impactFactor').get(mag)[0]['factor']
                    row.append(factor)
                elif i =='institution':
                    reference = ''
                    if obj.getField(i).get(obj):
                        reference = obj.getField(i).get(obj).getName()
                    row.append(reference)
                elif i == 'worksPerYear':
                    dates = ['%s - %s' % (j['year'], j['works']) for j in obj.getField(i).get(obj)]
                    row.append('<br>'.join(dates))
                elif i in ['event_date', 'begin_date', 'end_date', 'graduation_date']:
                    row.append(obj.getField(i).getFormattedDate(obj))
                elif i == 'institutionCountry':
                    vocabulary = obj.getField(i).Vocabulary(obj)
                    row.append(vocabulary.getValue(obj.getField(i).get(obj)))
                elif i == 'authorThesis':
                    names = []
                    for d in obj.getField(i).get(obj):
                         names.append(' '.join([d['firstname'], d['lastname1'], d['lastname2']]))
                    row.append(','.join(names))
                elif i == 'sede':
                    try:
                        return obj.sede
                    except Exception:
                        pass
                    ownerid = obj.aq_parent.aq_parent.id
                    # ids = [j for j in obj.getField('creators').get(obj)]
                    brains = self.portal_catalog(portal_type='FSDPerson', id=ownerid)
                    if brains:
                        row.append(brains[0].getObject().sede)
                    else:
                        row.append('')

                elif i in vocabulary_fields:
                    value = obj.getField(i).Vocabulary().getValue(obj.getField(i).get(obj))
                    row.append(value)

                elif i == 'country':
                    value = obj.getCountriesVocabulary().getValue(obj.getField(i).get(obj))
                    row.append(value)

                else:
                    row.append(obj.getField(i).get(obj))
            data.append((obj.absolute_url(), row))
        return data

    def matchContent(self, form, atype, sedes):
        site = getSite()
        #TODO: path must be dinamic
        path = ('acerca-de', 'estructura-interna', 'secretaria-academica', 'informes', 'investigadores', '2011')
        folder = site.unrestrictedTraverse('/'.join(path))

        if self.context.getRutaReportes() is not None:
            folder = self.context.getRutaReportes()

        # get ids to search in
        usersbysede = self.usersBySede(folder.objectIds())
        ids = [j for i in sedes for j in usersbysede[i]]
        # get items to search in
        brains = []
        # gil = 1

        
        for id in ids:
            query = {'portal_type': atype,
                     'path': {'query': '/'.join(folder[id].getPhysicalPath())}}
            # if not self.portal_catalog(query):
            #     print '%d %s' % (gil, id)
            #     gil = gil + 1
            brains.extend(self.portal_catalog(query))
        # get match items
        objects = []
        for brain in brains:
            obj = brain.getObject()
            match = True
            for key, value in form.iteritems():
                # make sure value is a list
                if not isinstance(value, ListType):
                    value = [value]
                func = getattr(obj, key, None)
                if callable(func) and not func() in value:
                    match = False
                    break
            if match:
                objects.append(obj)
        return objects

    #('C.U.', 'Cuernavaca', 'Juriquilla', 'Morelia'),
    def usersBySede(self, ids):
        brains = self.portal_catalog(portal_type='FSDPerson', id=ids)
        users ={'df': [], 'matcuer': [], 'matjuriquilla': []}
        for brain in brains:
            if 'CU' in brain.getClassificationNames:
                users['df'].append(brain.id)
            elif 'Cuernavaca' in brain.getClassificationNames:
                users['matcuer'].append(brain.id)
            elif 'Juriquilla' in brain.getClassificationNames:
                users['matjuriquilla'].append(brain.id)
                
        return users
