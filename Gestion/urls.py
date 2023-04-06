from django.urls import path

from Gestion import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('perfil/', views.perfil, name = "perfil"),
    path('modificarPerfil/', views.modificarPerfil, name = "modificarPerfil"),
    path('misviajes/', views.misviajes, name = "misviajes"),
    path('amigos/', views.amigos, name = "amigos"),
    path('modificarImgPerfil/', views.modificarImgPerfil, name = "modificarImgPerfil"),
    path('destinoDetalles/<int:ciudad_id>/', views.destinoDetalles, name = "destinoDetalles"),
    # viajes
    path('crearViaje/', views.crearViaje, name = "crearViaje"),
    path('verViaje/<int:viaje_id>/', views.verViaje, name = "verViaje"),
    path('modificarViaje/', views.modificarViaje, name = "modificarViaje"),
    path('viajesGestionar/', views.viajesGestionar, name = "viajesGestionar"),
    path('viajes/', views.misviajes, name = "viajestab"),
    path('viajesAceptar/<int:viaje_id>/', views.viajeAceptar, name = "viajesAceptar"),
    path('viajesRechazar/<int:viaje_id>/', views.viajeRechazar, name = "viajesRechazar"),
    # amigos
    path('seguidos/', views.seguidos, name = "seguidos"),
    path('seguidores/', views.seguidores, name = "seguidores"),
    path('amigosSolicitudes/', views.amigosSolicitudes, name = "amigosSolicitudes"),
    path('amigosBuscar/<int:viaje_id>/', views.amigosBuscar, name = "amigosBuscar"),
    path('amigosAceptar/<int:amigo_id>/', views.amigoAceptar, name = "amigosAceptar"),
    path('amigosRechazar/<int:amigo_id>/', views.amigoRechazar, name = "amigosRechazar"),
    path('amigosAgregar/', views.amigosAgregar, name = "amigosAgregar"),
    path('SeguirUsuarios/', views.SeguirUsuarios, name = "SeguirUsuarios"),
]