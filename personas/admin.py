from django.contrib import admin
from .models import Persona, Ciudad, Contacto

admin.site.register(Ciudad)
admin.site.register(Persona)
admin.site.register(Contacto)