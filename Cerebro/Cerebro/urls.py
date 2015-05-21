from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Cerebro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'appCerebro.views.home', name='home'),
    #el r'^$ hace que sea la pagina de inicio
    #y llama a la definicion HOME que esta en "appCerebro.views.py"
    url(r'^admin/', include(admin.site.urls)),
    #la siguiente URL es para meter datos en la BD    
    url(r'^api/upload/', 'appCerebro.views.api', name='api'),
    url(r'^proyectos/', 'appCerebro.views.proyectos', name='proyectos'),

#Espacio de prueba
    url(r'^tecnico/$', 'appCerebro.views.vistaTecnico', name='tecnico'),
    url(r'^doctor/$', 'appCerebro.views.vistaDoctor', name='doctor'),
    url(r'^paciente/$', 'appCerebro.views.vistaPaciente', name='paciente'),

    #url(r'^anadirProyecto1/$', 'appCerebro.views.vistaAnadirProyecto1', name='anadirProyecto1'),
    url(r'^anadirProyecto/$', 'appCerebro.views.vistaAnadirProyecto11', name='anadirProyecto11'),
    url(r'^(?P<nombreProyecto>[A-Za-z]+[0-9]+)/detalle/$', 'appCerebro.views.vistaProyecto', name='detalle'),
    url(r'^(?P<nombreProyecto>[A-Za-z]+)/detalle/$', 'appCerebro.views.vistaProyecto', name='detalle'),
    url(r'^(?P<nombreProyecto>[0-9]+)/detalle/$', 'appCerebro.views.vistaProyecto', name='detalle'),

    url(r'^(?P<nombreProyecto>[A-Za-z]+[0-9]+)/modificacion/$', 'appCerebro.views.modificarProyecto', name='modificar'),
    url(r'^(?P<nombreProyecto>[A-Za-z]+)/modificacion/$', 'appCerebro.views.modificarProyecto', name='modificar'),
    url(r'^(?P<nombreProyecto>[0-9]+)/modificacion/$', 'appCerebro.views.modificarProyecto', name='modificar'),
    
    #Para Eliminar (lo tengo por miedo):
    #url(r'^vistaProyecto/$', 'appCerebro.views.vistaProyecto', name='vistaProyecto'),    

#Fin de espacio de prueba

    url(r'^ejercicios/', 'appCerebro.views.ejercicios', name='ejercicios'),
    url(r'^datos/', 'appCerebro.views.datos', name='datos'),
    url(r'^datos/(?P<ejercicio>[^/]+)/$', 'appCerebro.views.datos', name='datos'),
	#url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
)
