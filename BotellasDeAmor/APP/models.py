from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.models import Group, Permission
import datetime
# Create your models here.

class CustomeUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("El E-mail que ha ingresado no es valido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = CustomeUserManager()
    
    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=['name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
    
class Merchandise(models.Model):
    consecutive_number = models.PositiveIntegerField(unique=True)
    weight = models.FloatField(default=0)  # Asegúrate de que el valor por defecto sea 0

    def __str__(self):
        return f"Merchandise {self.consecutive_number}"

class Foto(models.Model):
    PHOTO_CHOICES = [
        ("Remisión", "Remisión"),
        ("Pesajes", "Pesajes"),
        ("Descargue", "Descargue"),
        ("Puntos de acopio", "Puntos de acopio"),
    ]
    MATERIAL_CHOICES = [
        ("Botellas de Amor", "Botellas de Amor"),
        ("Otros Materiales", "Otros Materiales"),
    ]
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='uploads/product/')
    photoType = models.CharField(max_length=255, choices=PHOTO_CHOICES, default="Remisión")
    date = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=255)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    punto_acopio = models.CharField(max_length=255, default='', blank=True)
    weight = models.FloatField(null=True, blank=True)
    material_type = models.CharField(max_length=255, choices=MATERIAL_CHOICES, default="Botellas de Amor")  # Nuevo campo

    def __str__(self):
        return self.name