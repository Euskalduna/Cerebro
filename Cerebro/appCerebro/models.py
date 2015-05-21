from django.db import models

# Create your models here.

class Proyecto(models.Model):

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	
	def __unicode__(self):
		return "" + self.nombre

class Variable(models.Model):
	VAR_TYPE = ((1,'INT'),(2,'DATE'),(3,'DATETIME'),(4,'VARCHAR'),(5,'FLOAT'))
	#En VAR_TYPE igual poner boolean
	nombre = models.CharField(max_length=100)
	tipo =  models.IntegerField(choices=VAR_TYPE)

	def __unicode__(self):
		return "" + self.nombre + " " + str(self.VAR_TYPE[self.tipo-1][1])

class Ejercicio(models.Model):

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	tipo = models.CharField(max_length=100)
	#ejercicio= models.ForeignKey(Ejercicio)
	proyecto = models.ForeignKey(Proyecto)
	variables = models.ManyToManyField(Variable)
	
	def __unicode__(self):
		return "" + self.proyecto.nombre + " - " + self.nombre

class Usuario(models.Model):
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	descripcion = models.TextField()
	proyectos = models.ManyToManyField(Proyecto)
	def __unicode__(self):
		return "" + self.nombre

class Realizacion(models.Model):
	fecha = models.DateTimeField()
	usuario = models.ForeignKey(Usuario)
	ejercicio = models.ForeignKey(Ejercicio)

	def __unicode__(self):
		return "" + self.usuario.nombre + " " + self.ejercicio.proyecto.nombre + " "  + self.ejercicio.nombre + " " + str(self.fecha)

class Datos(models.Model):
	realizacion = models.ForeignKey(Realizacion)
	variable = models.ForeignKey(Variable)
	
	nivel = models.IntegerField()
	valor = models.CharField(max_length=100)

	class Meta:
		unique_together = (("realizacion", "variable"),)