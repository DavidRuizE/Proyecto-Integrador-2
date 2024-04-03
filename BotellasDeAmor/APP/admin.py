from django.contrib import admin
from .models import *

# Register your models here.

class FotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'photoType', 'date', 'place']  # Include 'date' here

admin.site.register(Foto, FotoAdmin)
admin.site.register(User)