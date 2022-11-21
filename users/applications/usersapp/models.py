import email
from re import M
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES =(
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
         )

    username = models.CharField(max_length=10, unique=True)
    email= models.EmailField()
    names = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length= 1, choices=GENDER_CHOICES, blank=True)
    codregistro= models.CharField(max_length=6, blank=True)
    #Cuando se crea un usaurio no tendra accesso a la consila ded administracion, es requerido por la funcion create del Manager
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    #el login se va a realizar con
    USERNAME_FIELD ='username'

    #para que la consula solicite el email
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.names + ' ' + self.last_name
