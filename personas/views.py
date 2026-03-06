from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import ProtectedError
from .models import Persona, Ciudad, Contacto

# ✅ Verificación de superusuario
def solo_superusuario(user):
    return user.is_active and user.is_superuser

# ------------------------------------------------------------------ #
# INICIO Y CONTACTO (públicos)
# ------------------------------------------------------------------ #

def inicio(request):
    total_personas = Persona.objects.count()
    total_ciudades = Ciudad.objects.count()
    return render(request, 'personas/inicio.html', {
        'total_personas': total_personas,
        'total_ciudades': total_ciudades
    })

def contacto(request):
    enviado = False
    if request.method == 'POST':
        nombre  = request.POST['nombre']
        correo  = request.POST['correo']
        mensaje = request.POST['mensaje']
        Contacto.objects.create(nombre=nombre, correo=correo, mensaje=mensaje)
        enviado = True
    return render(request, 'personas/contacto.html', {'enviado': enviado})

# ------------------------------------------------------------------ #
# PERSONAS (protegidas)
# ------------------------------------------------------------------ #

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'personas/lista_personas.html', {'personas': personas})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def crear_persona(request):
    ciudades = Ciudad.objects.all()
    error = None
    if request.method == 'POST':
        documento = request.POST['documento']
        nombre    = request.POST['nombre']
        apellido  = request.POST['apellido']
        direccion = request.POST['direccion']
        correo    = request.POST['correo']
        ciudad    = Ciudad.objects.get(id=request.POST['ciudad'])

        if Persona.objects.filter(documento=documento).exists():
            error = f'Ya existe una persona con el documento {documento}.'
        else:
            Persona.objects.create(
                documento=documento, nombre=nombre, apellido=apellido,
                direccion=direccion, correo=correo, ciudad=ciudad
            )
            messages.success(request, f'✅ Persona "{nombre} {apellido}" creada exitosamente.')
            return redirect('lista_personas')

    return render(request, 'personas/form_persona.html', {'ciudades': ciudades, 'error': error})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def editar_persona(request, id):
    persona  = get_object_or_404(Persona, id=id)
    ciudades = Ciudad.objects.all()
    if request.method == 'POST':
        persona.documento = request.POST['documento']
        persona.nombre    = request.POST['nombre']
        persona.apellido  = request.POST['apellido']
        persona.direccion = request.POST['direccion']
        persona.correo    = request.POST['correo']
        persona.ciudad    = Ciudad.objects.get(id=request.POST['ciudad'])
        persona.save()
        messages.success(request, f'✅ Persona "{persona.nombre} {persona.apellido}" actualizada correctamente.')
        return redirect('lista_personas')
    return render(request, 'personas/form_persona.html', {'persona': persona, 'ciudades': ciudades})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    if request.method == 'POST':
        nombre = f"{persona.nombre} {persona.apellido}"
        persona.delete()
        messages.success(request, f'🗑️ Persona "{nombre}" eliminada correctamente.')
        return redirect('lista_personas')
    return render(request, 'personas/eliminar_persona.html', {'persona': persona})

# ------------------------------------------------------------------ #
# CIUDADES (protegidas)
# ------------------------------------------------------------------ #

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def lista_ciudades(request):
    ciudades = Ciudad.objects.all()
    return render(request, 'personas/lista_ciudades.html', {'ciudades': ciudades})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def crear_ciudad(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        Ciudad.objects.create(nombre=nombre)
        messages.success(request, f'Ciudad "{nombre}" creada exitosamente.')
        return redirect('lista_ciudades')
    return render(request, 'personas/form_ciudad.html', {})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def editar_ciudad(request, id):
    ciudad = get_object_or_404(Ciudad, id=id)
    if request.method == 'POST':
        ciudad.nombre = request.POST['nombre']
        ciudad.save()
        messages.success(request, f' Ciudad "{ciudad.nombre}" actualizada correctamente.')
        return redirect('lista_ciudades')
    return render(request, 'personas/form_ciudad.html', {'ciudad': ciudad})

@login_required(login_url='login')
@user_passes_test(solo_superusuario, login_url='login')
def eliminar_ciudad(request, id):
    ciudad = get_object_or_404(Ciudad, id=id)
    if request.method == 'POST':
        try:
            nombre = ciudad.nombre
            ciudad.delete()
            messages.success(request, f'Ciudad "{nombre}" eliminada correctamente.')
            return redirect('lista_ciudades')
        except ProtectedError:
            return render(request, 'personas/eliminar_ciudad.html', {
                'ciudad': ciudad,
                'error': f'No se puede eliminar "{ciudad.nombre}" porque tiene personas asociadas.'
            })
    return render(request, 'personas/eliminar_ciudad.html', {'ciudad': ciudad})