# -*- coding: utf-8 -*-
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from matem.cvreports.browser.utils import listaAtributos
from matem.cvreports import cvreportsMessageFactory as _
from DateTime import DateTime
from UNAM.imateCVct.interfaces import ICVReportUtility
from zope.component import getUtility
import re
# import psycopg2

RESULTADO = [{'title': 'Structural Analysis of Complex Networks',
'autores': 'Joanna Ellis-Monaghan and Criel Merino',
'Investigador': 'Criel Merino López',
'path': 'fsd/merino/cv/cvbookchapterfolder/capituloreference.2008-12-05.1729645803',
'Capítulo': 'Graph polynomials and their applications I: the Tutte polynomial',
'Editor': 'Matthias Dehmer',
'Editorial': 'Birkhäuser',
'País': 'Germany',
'Líneas de Investigación': '05-xx Combinatoria',
'Fecha de publicación': '----/----/----',
'Notas': u'Aceptado pero todavia no publicado'},
{'title': 'Structural Analysis of Complex Networks',
'autores': 'Joanna Ellis-Monaghan and Criel Merino',
'Investigador': 'Criel Merino López',
'Capítulo': 'Graph polynomials and their applications I: the Tutte polynomial',
'Editor': 'Matthias Dehmer',
'Editorial': 'Birkhäuser',
'País': 'Germany',
'Líneas de Investigación': '05-xx Combinatoria',
'Fecha de publicación': '----/----/----',
'Notas': 'Aceptado pero todavía no publicado',
'path': '/infomatem/cv'}]

ERESULTADO = {'Total': 15}

TRESULTADO = {'header': ['Titulo', 'Autores', 'Investigador','path','Capítulo','Editor','Editorial','País','Líneas de Investigación','Fecha de publicación','Notas'],
'data': [['111 Structural Analysis of Complex Networks','Joanna Ellis-Monaghan and Criel Merino','Criel Merino López','fsd/merino/cv/cvbookchapterfolder/capituloreference.2008-12-05.1729645803','Graph polynomials and their applications I: the Tutte polynomial','Matthias Dehmer','Birkhäuser','Germany','05-xx Combinatoria','----/----/----','Aceptado pero todavía no publicado'],['2. Structural Analysis of Complex Networks','Joanna Ellis-Monaghan and Criel Merino','Criel Merino López','capituloreference.2008-12-05.1729645803','Graph polynomials and their applications I: the Tutte polynomial','Matthias Dehmer','Birkhäuser','Germany','05-xx Combinatoria','----/----/----','Aceptado pero todavía no publicado']]}


class IReportView(Interface):
    """
    Report view interface
    """

    def test():
        """ test method """

    def datos():
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

    def search(self):
        forma = self.request.form
        form = forma.copy()
        # set current cv type
        content = self.context.getCvcontent()
        tipoderesultados = ''
        #sacamos los elemento innecesarios de form solo 1 de los existe
        try:
            tipoderesultados = form.pop('formato_view')
        except:
            print "Esto es de tipo tabla"

        try:
            tipoderesultados = form.pop('tabla_view')
        except:
            print "Esto es de tipo formato"

        #Seperamos el titulo ya que este se filtra por separado en caso de que
        #tenga
        titulo = ''
        try:
            titulo = form.pop('Title')
        except:
            print "No opcion de busqeuda por titulo"

        #Separamos los elemento de la forma que nos indica los elementos a mostrar
        elementos_a_mostrar = []

        for f in form.keys():
            if f.startswith('checkbox'):
                elementos_a_mostrar.append(f)
                form.pop(f)


        #Seperamos las fechas ese filtro se hara al final
        fechas = {}
        for f in form.keys():
            if f.startswith('from') or f.startswith('to'):
                fechas[f] = form.pop(f)

        #Seperamos los filtros con seleccion multiple
        multiples = {}
        for f in form.keys():
            if f.startswith('mul'):
                multiples[f] = form.pop(f)

        #Creamos la parte del query para filtrar los multiples
        filtros_multiples = ''
        for m in multiples.keys():
            fil_m = "( "
            mul = m.lstrip('mul_get').lower()
            if ( mul == 'authors' or mul == 'editors' ):
                #Este es un caso especial y debe ser tratado con cuidado
                #ya que lo que se pasa de la busqueda es un id no un nombre
                if isinstance(multiples[m], basestring) :
                    nombre = self.portal_catalog(id=multiples[m])[0].getObject()
                    name = nombre['firstName'] +" "+ nombre['lastName']
                    fil_m +=  "g"+mul +" like \'%"+name+"%\' ) "
                else:
                    for ele in multiples[m]:
                        nombre = self.portal_catalog(id=ele)[0].getObject()
                        name = nombre['firstName'] +" "+ nombre['lastName']
                        fil_m += "g"+mul +" like \'%"+name+"%\' OR "
                    fil_m = fil_m[:-3]
                    fil_m += ")"
            else:
                #Tenemso que checar si multoples[m] es una cadena o una lista
                #ya que si 1 solo elemento regresa una cadena si tiene mas una
                # lista
                if isinstance(multiples[m], basestring) :
                    fil_m +=  mul +" like \'%"+multiples[m]+"%\' ) "
                else:
                    for ele in multiples[m]:
                        fil_m += mul +" like \'%"+ele+"%\' OR "
                    fil_m = fil_m[:-3]
                    fil_m += ")"
            filtros_multiples += fil_m + " AND "
        filtros_multiples = filtros_multiples[:-4]

        #Tenemos los filtros "sencillos" en form si no son vacios
        #creamos la parte del query de estos filtros
        filtros_sencillos = ''
        for f in form.keys():
            if form[f] != '':
                filtros_sencillos += f.lstrip('get').lower() +" like \'%"+form[f]+"%\' AND "
        filtros_sencillos = filtros_sencillos[:-4]

        #Los filstros son los filtros_sencillo mas los filtros multiples
        #en caso de existir estos
        filtros = filtros_sencillos;
        if filtros_multiples != '':
            if filtros == '':
                filtros +=  filtros_multiples
            else :
                filtros += " AND " + filtros_multiples

        #Tenemos el query con los filtros sencillos
        #Si se agrego algun filtro se agrega WHERE... si no pues no
        if filtros != '':
            query = "SELECT * FROM " + content.lower() +" WHERE " + filtros
        else:
            query = "SELECT * FROM " + content.lower()

        #Le agregamos al query el title haciendo un join con la tabla de content
        #Si se agrego filtro por titulo lo hacemos
        if titulo != '':
            querycontitle = "SELECT content.title, content.path, contenttype.* FROM content JOIN ("+query+") AS contenttype ON content.content_id = contenttype.content_id WHERE content.title like \'%"+titulo+"%\';"
        else:
            querycontitle = "SELECT content.title, content.path, contenttype.* FROM content JOIN ("+query+") AS contenttype ON content.content_id = contenttype.content_id;"

        try:
            conn_string = "dbname='infomatem' user='plone' host='localhost' password='plone'"
            # conex = psycopg2.connect(conn_string)
        except:
            print "I am unable to connect to the database"
        # cur = conex.cursor()
        # cur.execute(querycontitle)
        # res = cur.fetchall()
        # cur.close()
        # # conex.close()

        #En este puno ya se tiene el resultado de la query con todos los campos
        #y con los filtros sencillos y  multiples falta filtrar por fecha y
        #remover los campos que no queremos que se muestren

        #Primero de cur.description obtenemos el nombre de los campos que se
        #obtuvieron en orden
        columnas = []
        for ele in cur.description:
            columnas.append(ele[0])

        #hacemos el filtro de las fechas
        #sacamos las keys de las fechas y las ordenamos
        #de esta forma la mitad que empizan con to estan en una mitad y las que
        #empiezan con from del otro y podemos recorrerlas al mismo tiempo
        #con el inice i y i+nf
        fechaskeys  = fechas.keys()
        fechaskeys.sort()
        nf = len(fechaskeys)/2
        for i in range(nf):
            #suponiendo que todas las fechas estan contruids igual
            #ej from_AcceptDate queremos pasarlo ao algo como accept_date
            #dejamos solo lo que este entre from_ y Date y le pegamos _date
            nombrefecha = ""
            if fechaskeys[i].lstrip('from_') == 'EndGraduationDate' :
                nombrefecha = 'endgraduation_date'
            else:
                lnf = re.findall('[A-Z][^A-Z]*', fechaskeys[i].lstrip('from_'))
                for j in range(len(lnf)):
                    nombrefecha += lnf[j].lower() + "_"
                nombrefecha = nombrefecha[:-1]
            #sacamos el index de esa fecha en las tuplas de resultado
            index = columnas.index(nombrefecha)
            ffrom = fechas[fechaskeys[i]]
            fto = fechas[fechaskeys[i+nf]]
            cv_utility=getUtility(ICVReportUtility)
            #Creamos las fechas deacuerdo a lo que tenemos si no tenemos nada
            #creamos la primera y ultima fecha pordefault
            #Suponemos que nos pasan en la forma estan creadas correctamente
            #TODO TALVEZ CACHAR SI ESTAN MAL CREADAS
            if ffrom != '' :
                affrom = ffrom.split('/')
                initialDate=cv_utility.dict2date(affrom[2], affrom[0], affrom[1], True)
            else:
                initialDate=cv_utility.dict2date('0', '0', '0', True)
            if fto != '' :
                afto = fto.split('/')
                endDate=cv_utility.dict2date(afto[2], afto[0], afto[1], False)
            else:
                endDate=cv_utility.dict2date('0', '0', '0', False)

            #Si no tenemos ni fecha inicial ni final entonces no hay que
            #filtrar por esta fecha
            if ffrom == '' and fto == '' :
                continue

            #Si tenemos alguna hay que filtrar
            #Vamos recorrer los resultado del ultimo al primero para poder ir
            #borrando los que no cumplan y no cambien los indexes

            rango = range(len(res))
            rango.reverse()
            for i in rango:
                #contruimos la fecha para el elemento a checar
                elemento = res[i]
                fechaE = elemento[index]
                fecha = fechaE.split('-')
                cv_utility=getUtility(ICVReportUtility)
                #Si es una fecha invalida entonces solo se toma el año para crearla
                #y se crea por default en el primero de enero de ese año
                try :
                    elemdate=cv_utility.dict2date(fecha[0], fecha[1], fecha[2], True)
                except:
                    elemdate = cv_utility.dict2date(fecha[0], '0', '0', True)
                elementocumple = True
                #si tenemos fecha inicial y final comparamos que este entre las2
                if ffrom != '' and fto != '' :
                    elementocumple = (elemdate >= initialDate) & (elemdate <= endDate)
                #si solo tenemos final o incial comparamos respectivamente
                else:
                    #si tenemos inicial entonces la fecha debe ser mayor
                    if ffrom != '' :
                        elementocumple = elemdate >= initialDate
                    #si no tenemos inicial entonces tnemso final y debe ser menor
                    else:
                        elementocumple = elemdate <= endDate

                #Si el elementonocumple con el rango de fechas lo borramos
                if not elementocumple :
                    res.remove(elemento)

        #Si res la lista de los elemtnos encontras es vacio regresamos vacio
        #si tiene algo regresamo sun diccinario con los elemtos requeridos

        if len(res) == 0 :
            return []


        #Ya tenemos todos los filtros realizados solo falta regresar unicamente
        #los campos que se nos piden
        #TODO casos espeicales para y researchtopic
        portalurl = self.portal.portal_url()
        if tipoderesultados == 'Vista con Formato':
            data = []
            for r in res :
                dic = {}
                dic["title"] = r[columnas.index("title")]
                dic["path"] = portalurl.rstrip("/infomatem") + r[columnas.index("path")]
                for ele in elementos_a_mostrar :
                    dato = ele.lstrip("checkbox_")
                    if dato.lower().find("date") > 0 :
                        nombrefecha = ""
                        if dato == 'EndGraduationDate' :
                            nombrefecha = 'endgraduation_date'
                        else:
                            lnf = re.findall('[A-Z][^A-Z]*', dato)
                            for i in range(len(lnf)):
                                nombrefecha += lnf[i].lower() + "_"
                            nombrefecha = nombrefecha[:-1]
                        index = columnas.index(nombrefecha)
                    else :
                        colname = dato.lstrip("get").lower()
                        if colname == 'authors' or colname == 'editors':
                            index = columnas.index("g"+colname)
                        else:
                            index = columnas.index(colname)
                    if dato == 'getResearchTopic' :
                        topics = r[index]
                        litopics = topics.split("\n")
                        strtopic = ""
                        for ele in litopics :
                            if ele != '' :
                                strtopic += self.portal_catalog(id=ele)[0].getObject()['title'] + ", \n"
                        dic[dato] = strtopic
                    else:
                        dic[dato] = r[index]
                data.append(dic)

            return data
        else:
            toshow = [key[9:] for key in elementos_a_mostrar]
            tabla = {'header': ['Titulo'] + toshow}
            data = []
            for r in res :
                row = [ (r[columnas.index("title")], portalurl.rstrip("/infomatem") + r[columnas.index("path")]), ]
                for ele in elementos_a_mostrar :
                    dato = ele.lstrip("checkbox_")
                    if dato.lower().find("date") > 0 :
                        nombrefecha = ""
                        if dato == 'EndGraduationDate' :
                            nombrefecha = 'endgraduation_date'
                        else:
                            lnf = re.findall('[A-Z][^A-Z]*', dato)
                            for i in range(len(lnf)):
                                nombrefecha += lnf[i].lower() + "_"
                            nombrefecha = nombrefecha[:-1]
                        index = columnas.index(nombrefecha)
                    else :
                        colname = dato.lstrip("get").lower()
                        if colname == 'authors' or colname == 'editors':
                            index = columnas.index("g"+colname)
                        else:
                            index = columnas.index(colname)
                    if dato == 'getResearchTopic' :
                        topics = r[index]
                        litopics = topics.split("\n")
                        strtopic = ""
                        for ele in litopics :
                            if ele != '' :
                                strtopic += self.portal_catalog(id=ele)[0].getObject()['title'] + ", \n"
                        row.append(strtopic)
                    else:
                        row.append(r[index])
                data.append(row)
            tabla['data'] = data
            return tabla



    def datos(self):

        return self.search()

    def archivos(self):
        """
        returns the number of elements that belongs to the list
        """
        return len(self.search())

    def statistic(self):
        """
        """
        return ERESULTADO

    def table(self):

        return self.search()
