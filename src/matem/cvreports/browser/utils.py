# -*- coding: utf-8 -*-
ARBITRAJES = 'CVRefereeing'
ARTICULOS = 'CVArticle'
ASISTENCIA_REUNIONES_ACADEMICAS = 'CVEvent'
CAPITULOS_LIBROS = 'CVBookChapter'
COMITES_ACADEMICOS = 'CVCommitte'
COMITES_EDITORIALES = 'CVEditorialCom'
CONFERENCIAS_PLENARIAS = 'CVConferencePlus'
CONFERENCIAS_MESAS = 'CVConference'
CONVENIOS = 'CVAgreement'
CURSOS = 'CVCourse'
INFRAESTRUCTURA = 'CVInfraestructure'
EDITOR_MEMORIAS = 'CVProceeding'
# INFORMES = ''
INVITADOS = 'CVGuest'
LIBROS = 'CVBook'
MAT_APOYO = 'CVTeachingAid'
MEMBRESIAS = 'CVMembership'
ORGANIZACION_EVENTOS = 'CVEventOrg'
FORMAS_TITULACION = 'CVQualification'
PATENTES = 'CVPatent'
PATROCINIOS = 'CVSponsorship'
PLANES_ESTUDIO = 'CVStudieProgram'
PREMIOS = 'CVAward'
PROTOTIPO = 'CVTechTransfer'
PUESTO_ACADEMICO = 'CVAcadStaffPosition'
REVISION_TRABAJOS = 'CVReview'
SEMINARIOS = 'CVFormationAct'
SOFTWARE = 'CVSoftware'
TESIS = 'CVThesis'
TRADUCCIONES = 'CVTranslation'
TUTORIAS = 'CVTutorship'
VISITAS = 'CVVisit'
# CITAS = ''
PROYECTOS = 'CVProject'

# TODO: El vocablario reporta 4 cosas que no estan en este diccionario.
# institucion, proyecto, reporte/informe, revista.

listaAtributos={
    ARBITRAJES: ['magazineRef', 'event_date'],
    ARTICULOS: ['status', 'articleType', 'referee', 'isnational',
            'researchTopic', 'publicationType'],
    ASISTENCIA_REUNIONES_ACADEMICAS: ['country', 'institution', 'title', 'audienceType'],
    CAPITULOS_LIBROS: ['country', 'researchTopic', 'authors', 'relatedProjects'],
    COMITES_ACADEMICOS: ['institution'],
    COMITES_EDITORIALES: ['commtype'],
    CONFERENCIAS_PLENARIAS: ['country', 'conftype', 'researchTopic'],
    CONFERENCIAS_MESAS: ['country', 'conftype', 'modality', 'assist', 'researchTopic'],
    CONVENIOS: ['internalCollaborators', 'institutions'],
    CURSOS: ['coursetype', 'level', 'researchTopic', 'semester', 'institution'],
    INFRAESTRUCTURA: ['institution'],
    EDITOR_MEMORIAS: ['editors', 'proceedingtype', 'status', 'researchTopic',
            'relatedProjects'],
    INVITADOS: ['title', 'institution'],
    LIBROS: ['researchTopic', 'status', 'country', 'materialType', 'booktype',
            'authors', 'booktype'],
    MAT_APOYO: ['aidType', 'level'],
    MEMBRESIAS: ['title'],
    ORGANIZACION_EVENTOS: ['instituteParticipation', 'eventType', 'researchTopic'],
    FORMAS_TITULACION: ['qualificationForm', 'institution', 'researchTopic'],
    PATENTES: ['isnational'],
    PATROCINIOS: ['sponshorshipType'],
    PLANES_ESTUDIO: ['institution', 'level'],
    PREMIOS: ['isnational', 'institution'],
    PROTOTIPO: ['isnational'],
    PUESTO_ACADEMICO: ['institution'],
    REVISION_TRABAJOS: ['organization'],
    SEMINARIOS: ['activityType', 'participationType', 'researchteaching_type',
            'level', 'speakto', 'researchTopic'],
    SOFTWARE: ['softtype', 'internalCollaborators'],
    TESIS: ['thesisType', 'status_thesis', 'level', 'researchTopic', 'institution'],
    TRADUCCIONES: ['title'],
    TUTORIAS: ['level', 'institution', 'researchTopic'],
    VISITAS: ['researchVisit', 'sabbaticalLeave', 'participationMeeting', 'institution'],
    PROYECTOS: ['internalCollaborators', 'sponsor', 'internalResponsible',
            'projectType', 'researchTopic'],
}
