from django.db import models

class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Persona(models.Model):
    documento = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    correo = models.EmailField()
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.nombre} - {self.correo}"