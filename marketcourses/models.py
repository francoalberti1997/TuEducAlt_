from typing import Any
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    image = models.ImageField(upload_to='marketcourses/static/marketcourses/img', blank=True, null=True)

    class Meta: 
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='marketcourses/static/marketcourses/img', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='marketcourses/static/marketcourses/img', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
#cambiando a ramab
    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000/' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000/' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000/' + self.thumbnail.url
            else:
                return ''
    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'jPEG', quality = 85)
        thumbnail = File(thumb_io)

#logos
class Archivos_pagina(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='marketcourses/static/marketcourses/img')


class Estudiantes(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    edad = models.IntegerField(null=True)
    mail = models.EmailField(null=True)
    imagen = models.ImageField(upload_to='marketcourses/static/marketcourses/img', blank=True, null=True, default=None)
    tiene_img = models.BooleanField(default=False, blank=True, null=True)
    lista_rates = [(1, "Muy bien"), (2, "Buena"), (3, "Mala")]
    estrellas = models.IntegerField(choices=lista_rates, blank=True, null=True, default=None)
    opiniones = models.CharField(max_length=80, blank=True, null=True, default=None)
    opinion_completa = models.BooleanField(default=False, blank=True)

    def __init__(self, *args, **kwargs):
        super(Estudiantes, self).__init__(*args, **kwargs)
        self.set_estudiantes()

    def set_estudiantes(self):
        if not self.tiene_imagen():
            self.opinion_completa = False
            return
        for field in self._meta.get_fields():
            if getattr(self, field.name) is None:
                self.opinion_completa = False
                return
        self.opinion_completa = True

    def tiene_imagen(self):
        if self.imagen:
            self.tiene_img = True
            return True
        else:
            self.tiene_img = False
            return False


# @receiver(pre_save, sender=Estudiantes)
# def asignar_usuario(sender, instance, **kwargs):
#     print("ingresando a ala SIGNAL")
#     if not instance.user:
#         instance.user = User.objects.create_user(username=instance.username, password=instance.password)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Estudiantes.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     try:
#         estudiantes = instance.estudiantes
#     except ObjectDoesNotExist:
#         estudiantes = Estudiantes.objects.create(user=instance)
#     estudiantes.save()