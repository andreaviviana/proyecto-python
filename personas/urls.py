from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',                            views.inicio,             name='inicio'),
    path('contacto/',                   views.contacto,           name='contacto'),

    #LOGIN 
    path('login/',  auth_views.LoginView.as_view(template_name='personas/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # PERSONAS (protegidas)
    path('personas/',                   views.lista_personas,     name='lista_personas'),
    path('personas/crear/',             views.crear_persona,      name='crear_persona'),
    path('personas/editar/<int:id>/',   views.editar_persona,     name='editar_persona'),
    path('personas/eliminar/<int:id>/', views.eliminar_persona,   name='eliminar_persona'),

    # CIUDADES (protegidas)
    path('ciudades/',                   views.lista_ciudades,     name='lista_ciudades'),
    path('ciudades/crear/',             views.crear_ciudad,       name='crear_ciudad'),
    path('ciudades/editar/<int:id>/',   views.editar_ciudad,      name='editar_ciudad'),
    path('ciudades/eliminar/<int:id>/', views.eliminar_ciudad,    name='eliminar_ciudad'),
]