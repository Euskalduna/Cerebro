from django.shortcuts import render
from appCerebro.models import Proyecto, Ejercicio, Variable, Usuario, Realizacion, Datos
from django.views.decorators.csrf import csrf_exempt
import json 
from django.utils import simplejson
from datetime import datetime  
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib import auth
import copy

#COSAS A PEDIR:
#anadirProyecto:
	#Problema con el select: como hago para coger el valor seleccionado????
	#cambiando para meter mas de un desarrollador

#vistaProyecto:
	#scrol en las tablas (si el scroll se puede disimular cuando no haga falta mejor)
	#lo del despliegue de las Tablas

#modificarProyecto:
	#anadir nuevos atributos
	#anadir propiedades en atributos existentes
	#cambiar nombre de atributos
	#cambiar nombre de propiedades
	#eliminar atributos
	#eliminar propiedades

#eliminarProyecto:

#procesamiento de Datos:



import os
#import pymongo
import pymongolab


#from pymongo import MongoClient
from pymongolab import MongoClient
from django.conf import settings
#client=pymongo.MongoClient("mongodb://root:evida0@ds037581.mongolab.com:37581/cerebromongo")
client=MongoClient("tQTYL-n7i4oG6QsWO3bua4GRt_CYtX53")
db=client['cerebromongo']


# Create your views here.
projectCol = db["proyectos1"]
projectCollection=db["proyectos"]
userCol= db["usuarios"]

@csrf_exempt
def home(request):
	
	username=request.POST.get("username","")
	password=request.POST.get("pass","")
	user=auth.authenticate(username=username,password=password) #si no funciona en vez de nick usar "username"
	
	if user is not None and user.is_active:
		auth.login(request,user)

		#Hacer la distincion de grupos:
			#Si es desarrollador le envio a X pagina 
			#Si es medico le envio a Y pagina
	
		grupo1=user.groups.filter(name="desarrolladores").exists()
		grupo2=user.groups.filter(name="doctores").exists()
		grupo3=user.groups.filter(name="pacientes").exists()
		if grupo1:
			return HttpResponseRedirect('/tecnico/')
		elif grupo2:
			return HttpResponseRedirect('/doctor/')
		elif grupo3:
			return HttpResponseRedirect('/paciente/')
	#else:
		#Manejo el error de login
	return render_to_response('index2.html')
#------------------------------------------------------------------------------------
#Limitar el acceso de los grupos. Creo que tengo que crear en cada grupo 
#permisos del estilo "is_developer" y despues utilizar @permission_required('is_developer')
#(esto de @permission_required esta en la documentacion de la autenticacion de Django por el final)
@csrf_exempt
def vistaTecnico(request):
	
	proyectos = list(projectCollection.find())
	longitud=len(proyectos)
	listaProyectos=[]
	listaParticipantes=[]
	listaParticipantesPrueba=[]
	context={}
	
	listaUsuarios=[]
	listaDesarrolladores=[]
	listaDoctores=[]
	for p in range(0,longitud):
		proy=proyectos[p]		
		#print proy
		proyecto = {"nombre": proy['nombreProyecto']}
		listaProyectos.append(proyecto)
		cargadoParticipantes(proy,'desarrollador',listaParticipantesPrueba,listaDesarrolladores)

	context.update({"proyectos": listaProyectos})
	context.update({"participantes":listaParticipantesPrueba})	
	#print "El context despues"
	#print context
	return render(request, 'vistaTecnico.html', context)

def cargadoParticipantes(proy,tipo,listaParticipantesPrueba,lista):	
	#FALLA CON LOS DESARROLLADORES DUPLICADOS!!!

	if tipo=='usuario':
		clave='usuarios'
		claveDict='user'
	elif tipo=='desarrollador':
		clave='nombreDesarrolladores'
		claveDict='dev'
	elif tipo=='doctor':
		clave='doctores'
		claveDict='doc'
	
	numBucle=len(proy[clave])	
	for i in range(0,numBucle):
		encontrado=False
		#participante={"user"+str(len(listaParticipantes)+1): proy['usuarios'][i]}
		participante={claveDict: proy[clave][i]}		

		for a in range(0,len(lista)):			
			nombreLista=lista[a]				
			#if nombreLista['user'+str(a+1)]==participante['user'+str(len(listaParticipantes)+1)]:
			if nombreLista[claveDict]==participante[claveDict]:
				encontrado=True
		if encontrado==False:
			lista.append(participante)
			listaParticipantesPrueba.append(participante)




@csrf_exempt
def vistaDoctor(request):
	return render_to_response('vistaDoctor.html')

@csrf_exempt
def vistaPaciente(request):
	return render_to_rasponse('vistaPaciente.htmA')

@csrf_exempt
def vistaAnadirProyecto11(request):
	
	proyecto={}
	nombreProyecto=str(request.POST.get("nombreProyecto",""))
	proyecto.update({'nombreProyecto':nombreProyecto})	

	nombreDesarrolladores=str(request.POST.get("nombreDesarrolladores",""))
	#print nombreDesarrolladores
	listaDesarrolladores=nombreDesarrolladores.split(",")#
	#print listaDesarrolladores
	proyecto.update({'nombreDesarrolladores':listaDesarrolladores})#
	#listaAtributos=[] #Posicion original de esa variable
	#print proyecto

	descripcion=str(request.POST.get("descripcionProyecto",""))#no meter enies en el campo
	proyecto.update({'descripcion':descripcion})	

	listaAtributos=[]

	numAtributos=request.POST.get("numeroAtributos","0")
	if numAtributos=="":
		numAtributos=0
	print "numeroAtributos: "+str(numAtributos)
	numAtributos=int(numAtributos)


	numPropiedades=request.POST.get("numeroPropiedades","0,")
	numPropiedades=numPropiedades.split(",")
	if len(numPropiedades)!=numAtributos:
		dif=numAtributos-len(numPropiedades)
		for z in range(0,dif):
			numPropiedades.insert(numAtributos-dif+z,"0")
	
	print "tras las modificaciones"
	print numPropiedades
	print len(numPropiedades)
	if len(numPropiedades)==1:
		
		if numPropiedades[0]=="":
			print "dentro!!!"
			numPropiedades[0]="0"
			print numPropiedades
	

	for i in range(0,numAtributos):
		x=i+1
		atributo={}
		listaPropiedades=[]
		nombreAtributo=str(request.POST.get("nombreAtributo"+str(x),""))		
		atributo.update({'nombreAtributo':nombreAtributo})
		propiedades=int(numPropiedades[i])


		for a in range(0,propiedades):			
			y=a+1
			propiedad={}			
			nombrePropiedad=str(request.POST.get("nombreAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'nombrePropiedad':nombrePropiedad})

			tipoPropiedad=str(request.POST.get("tipoAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'tipoPropiedad':tipoPropiedad})

			valorPropiedad=str(request.POST.get("valorAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'valorPropiedad':valorPropiedad})			
			listaPropiedades.append(propiedad)
		
		atributo.update({'propiedades':listaPropiedades})		
		listaAtributos.append(atributo)

	#este update deberia de hacerse despues de tener todos los atributos en la lista
	proyecto.update({'atributos':listaAtributos})
	print proyecto
	#HARIA EL INSERT
	if nombreProyecto!="":
		projectCollection.insert(proyecto)#comprobar que funciona
	#else:
		#AVISAR DE QUE TIENE QUE METER EL NOMBRE

	#EN PRUEBAS (las siguientes 2 lineas)
	if request.method=='POST':
		return HttpResponseRedirect('/tecnico/')

	return render_to_response('anadirProyecto11.html')	

#Siguiente paso: vista en detalle de X proyecto 
#Siguiente paso: forma de modificar los datos desde la pagina
	#cuando termine de REGISTRAR o MODIFICAR algun proyecto, el submit redirige
	#a la misma URL (para que se ejecute el mismo metodo) pero en vez de 
	#return render(request,'modificarProyecto.html',context) deberia de ser un
	#Httpredirect(/tecnico/) o algo asi (y ya si pongo un mensaje de "se ha actualizado" la hostia)


#como pongo los datos? creo unas tablas cuyo tamanio dependa de los datos u otra cosa?
#como agrego usuarios a un proyecto? (el de jon tiene pacientes ya metidos)
#les pongo un "usuarios" y segun el nombre busque "documents" que se correspondan?
#en el caso del robot de leire, los datos de los usuarios no los almaceno en el docs de usuarios

#como hago el envio/recepcion de datos?
#hago una URL en el url.py para que llame a X metodo? y luego ahi cojo su JSON y hago 
#lo que necesite y por ultimo envio las mods al MONGOLAB

#eliminar seria tan sencillo como eliminar el docs del proyecto? o tendria que tener en cuenta algo mas?
#ej: si en "usuario" hay un campo con los nombres de los proyectos en los que esta metido
#tendria que recorrer ese campo y eliminar el nombre que coincida con el nombre del proyecto para eliminar
#eso de generar informes...graficas????

#@login_required es para el log sea requerido (como dice zopenco)
#en el caso de la API csrf_exempt (en los de mas no)
#RELACIONES: meter en el tipo??? (similar) 
#
@csrf_exempt
def vistaProyecto(request,nombreProyecto):
	
	print "nombre del proyecto"
	print nombreProyecto
	proyectos = list(projectCollection.find())
	longitud=len(proyectos)
	#cojo los proyectos
	# parseo hasta encontrar aquel que coincide con el nombre
	#una vez encontrado hago las cosas nazis

	for p in range(0,longitud):

		proy=proyectos[p]
		nombreP=proy['nombreProyecto']

		if nombreP==nombreProyecto:
			context=proy
			print "dddddddddddddddddd"
			print context
			#busco longitud de desarrolladores
			#hago un for y los meto en una lista listaDesarrolladores=[]
			#meto la lista en context

			#descripcion=proy['descripcion']
			#lo meto en el context

			#busco longitud de atributos
			#hago un for
				#busco el nombre de los atributos
	return render(request,'vistaProyecto.html',context)

def eliminarProyecto(request):
	#tendria que recibir 2 parametros, el request y el NOMBRE PROYECTO(variable con el nombre de nombreP)

	#projectCollection.remove({'nombreProyecto':nombreP}) #asi elimino el proyecto pero y los usuarios???
	return HttpResponseRedirect('/tecnico/')

	#tras el borrado se redirigira a la vistaTecnico que NO debe conservar lo borrado
@csrf_exempt
def modificarProyecto(request, nombreProyecto):

	#modificacion={"$set":cambios}
	#print "modificacion"
	#print modificacion
	#http://blog.pythonisito.com/2012/01/moving-along-with-pymongo.html

	context={}
	clave={"nombreProyecto":str(nombreProyecto)}
	proyectos = list(projectCollection.find())
	longitud=len(proyectos)
#------------------------------------------------------------------------------------------------
	#para rellenar las casillas
	for p in range(0,longitud):
		proy=proyectos[p]
		nombreP=proy['nombreProyecto']
		
		if nombreP==nombreProyecto:
			context=proy
#------------------------------------------------------------------------------------------------
	#cojo las casillas comunes
	#cambios=context
	cambios={}
	cambios=copy.deepcopy(context)
	print "El original"
	print cambios
	listaAtributos=[]
	

	nProy=str(request.POST.get("nombreProyecto",""))	
	cambios.update({"nombreProyecto":nProy})

	nombreDesarrolladores=str(request.POST.get("nombreDesarrolladores",""))	
	listaDesarrolladores=nombreDesarrolladores.split(",")#
	#cambios.update({"nombreDesarrolladores":nombreDesarrolladores})

	descripcion=str(request.POST.get("descripcionProyecto",""))#OJO! esta vacio de momento!!!
	cambios.update({"descripcion":descripcion})
	
	#--------------------------------------------------------
	#Sin Modificacion
	numAtributos=request.POST.get("numeroAtributos","0")
	if numAtributos=="":
		numAtributos=0
	numAtributos=int(numAtributos)

	numPropiedades=request.POST.get("numeroPropiedades","0,")
	numPropiedades=numPropiedades.split(",")
	if len(numPropiedades)!=numAtributos:
		dif=numAtributos-len(numPropiedades)
		for z in range(0,dif):
			numPropiedades.insert(numAtributos-dif+z,"0")
	
	if len(numPropiedades)==1:		
		if numPropiedades[0]=="":
			numPropiedades[0]="0"
	#--------------------------------------------------------
	#Con Modificacion

	mNumAtributos=request.POST.get("mNumeroAtributos","0")
	if mNumAtributos=="":
		mNumAtributos=0
	mNumAtributos=int(mNumAtributos)

	
	#cojo las casillas de los atributos ANADIDOS
#------------------------------------------------------------------------------------------------
	for i in range(0,numAtributos):
		x=i+1
		atributo={}
		listaPropiedades=[]
		nombreAtributo=str(request.POST.get("nombreAtributo"+str(x),""))		
		cambios["atributos"].append({'nombreAtributo':nombreAtributo})
		propiedades=int(numPropiedades[i])

		for a in range(0,propiedades):	
			print "dentro del for"		
			y=a+1
			propiedad={}			
			nombrePropiedad=str(request.POST.get("nombreAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'nombrePropiedad':nombrePropiedad})

			tipoPropiedad=str(request.POST.get("tipoAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'tipoPropiedad':tipoPropiedad})
			
			#-----------------------------------
			valorPropiedad=str(request.POST.get("valorAtributo"+str(x)+"Propiedad"+str(y),""))
			propiedad.update({'valorPropiedad':valorPropiedad})			
			listaPropiedades.append(propiedad)
			#-----------------------------------
		
		for l in cambios["atributos"]:
			if l["nombreAtributo"]==nombreAtributo:
				#print "OOOOOOOOOOO"
				#print l
				l.update({'propiedades':listaPropiedades})
			
		#cambios["atributos"][nombreAtributo].update({'propiedades':listaPropiedades})
		#atributo.update({'propiedades':listaPropiedades})	

		#listaAtributos.append(atributo)

	#este update deberia de hacerse despues de tener todos los atributos en la lista
	#cambios.update({'atributos':listaAtributos})
	
#------------------------------------------------------------------------------------------------
	#cojo las casillas de los atributos MODIFICADOS
#------------------------------------------------------------------------------------------------

	for i in range(0,mNumAtributos):
		x=i+1
		atributo={}
		listaPropiedades=[]

		nombreAtributo=str(request.POST.get("mNombreAtributo"+str(x),""))
		filtrado=str(request.POST.get("mLabelNombreAtributo"+str(x),""))
		'''
		print "SDLKFJASDLKFJSADLKFJSDLKFJSD"
		print "mLabelNombreAtributo"+str(x)
		print filtrado
		'''
		print "TTTTTTTR"
		print nombreAtributo
		

		for q in cambios["atributos"]:			
			if q["nombreAtributo"]==filtrado:
				q["nombreAtributo"]=nombreAtributo
				
				mNumPropiedades=request.POST.get("mNumeroPropiedades","0")
				mNumPropiedades=mNumPropiedades.split(",")
				mPropiedades=int(mNumPropiedades[i])
				print "NUMERO PROP"
				print mPropiedades

				print 
				y=1			
				#for a in q["propiedades"]:
				for a in range(0,mPropiedades):
					propiedad={}
					nombrePropiedad=str(request.POST.get("mNombreAtributo"+str(x)+"Propiedad"+str(y),""))
					tipoPropiedad=str(request.POST.get("mTipoAtributo"+str(x)+"Propiedad"+str(y),""))
					#a["nombrePropiedad"]=nombrePropiedad
					#a["tipoPropiedad"]=tipoPropiedad	
					print "EEEEEEE"				
					propiedad.update({"nombrePropiedad":nombrePropiedad})
					propiedad.update({"tipoPropiedad":tipoPropiedad})
					propiedad.update({"valorPropiedad":""})
					q["propiedades"].append(propiedad)

					print "RETWEQRWE"
					print propiedad
					y+=1			
	print
	print
	print "cambios AL FINAL"
	print cambios
	print
	print
#------------------------------------------------------------------------------------------------	
	
	modificacion={"$set":cambios}
	#print modificacion

	if nProy!="":
		print "el update"
		projectCollection.update(clave,modificacion)
	if request.method=='POST':
		return HttpResponseRedirect('/tecnico/')		
	return render(request,'modificarProyecto.html',context)

#------------------------------------------------------------------------------------
def api(request):
	if request.method == 'GET':
	    return HttpResponse("{ 'method': 'GET' }")
	elif request.method == 'POST':
		print request.body
		data = json.loads(request.body)
		response = {}
		response['method'] = "POST"

		#Comprobar campo proyecto
		try:
			data['proyecto']
		except KeyError:
			response['error'] = "Falta el nombre del proyecto"
			return HttpResponse(simplejson.dumps(response))

		try:
			pr = Proyecto.objects.get(nombre = data['proyecto'])
		except Proyecto.DoesNotExist:
			#response['error'] = "No existe el proyecto"
			#return HttpResponse(simplejson.dumps(response))
			pr = Proyecto.objects.create(nombre = data['proyecto'])

		
		#Comprobar campo ejercicio
		try:
			data['ejercicio']
		except KeyError:
			response['error'] = "Falta el nombre del ejercicio"
			return HttpResponse(simplejson.dumps(response))

		try:
			ej = Ejercicio.objects.get(nombre = data['ejercicio'], proyecto = pr)
		except Ejercicio.DoesNotExist:
			#response['error'] = "No existe el ejercicio para el proyecto " + pr.nombre
			#return HttpResponse(simplejson.dumps(response))
			ej = Ejercicio.objects.create(nombre=data['ejercicio'], proyecto = pr)

		#aqui tengo que haber creado por cojones variables ya 
		#Comprobar las variables del ejercicio
		#for v in ej.variables.all():
		#	try:
		#		data[v.nombre]
		print "algo"
		#	except KeyError:
				#response['error'] = "Falta la variable " + v.nombre
				#return HttpResponse(simplejson.dumps(response))
		print "voy a crear el ejercicio"
		var = Variable.objects.create(nombre='cosa', tipo=1)
		var2 = Variable.objects.create(nombre='asoc', tipo=1)
		ej.variables.add(var)
		ej.save()

		#Comprobar el campo de nivel
		try:
			data['nivel']
			if data['nivel'] == '':
				raise KeyError 
			try:
				int(data['nivel'])
			except ValueError:
				raise KeyError
		except KeyError:
			response['error'] = "Falta indicar el nivel del ejercicio"
			return HttpResponse(simplejson.dumps(response))

		#Comprobar el campo de jugador
		try:
			data['usuario']
			if data['usuario'] == '':
				raise KeyError 
		except KeyError:
			response['error'] = "Falta el nombre del jugador"
			return HttpResponse(simplejson.dumps(response))

		#Crear jugador si no existe
		try:
			u = Usuario.objects.get(nombre = data['usuario'])
		except Usuario.DoesNotExist:
			#response['error'] = "No existe el jugador con nombre " + ju.nombre
			u = Usuario.objects.create(nombre = data['usuario'])
		
		u.proyectos.add(pr)
		u.save()

		#Crear partida con la fecha actual y crear las puntuaciones para cada variable
		realizacion = Realizacion.objects.create(usuario = u, ejercicio = ej, fecha = datetime.now())
		print "fuera del for"
		for v in ej.variables.all():
			print "dentro del for"
			print v.nombre
			datos = Datos.objects.create(realizacion = realizacion, variable = v, nivel = int(data["nivel"]), valor = data[v.nombre])
			print "dentro del for2"			
		response['upload'] = 'OK'
		return HttpResponse(simplejson.dumps(response))
	elif request.method == 'DELETE':
	    return HttpResponse("{ 'method': 'DELETE' }")
	elif request.method == 'PUT':
	    return HttpResponse("{ 'method': 'PUT' }")


def proyectos(request):
	pr=Proyecto.objects.all()
	context = {"pr": pr} #meto todos los proyectos en una variable pr 
	return render(request, 'proyectos.html', context)

#	if request.method == 'POST':
#		return redirect('ejercicios', proyecto = request.POST.get("pr", ""))

def ejercicios(request):
	ej0=Ejercicio.objects.all()
	context = {"ej": ej0} #meto todos los proyectos en una variable pr 
	return render(request, 'ejercicios.html', context)

def datos(request, ejercicio):
	if ejercicio:
		ej = Ejercicio.objects.get(pk = ejercicio)
		partidas = Partida.objects.filter(ejercicio = ej)
		arrayDatos = []
		for p in partidas:
			ps = Datos.objects.filter(partida = p).select_related()
			for p1 in ps:
				arrayDatos.append(p1)

	context = {"arrayDatos": arrayDatos, "ejercicio": ej, "variables":ej.variables.all()}
	return render(request, 'datos.html', context)