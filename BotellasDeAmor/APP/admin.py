from django.contrib import admin
from .models import *

# Register your models here.


class FotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'photoType', 'date', 'place', 'material_type', 'merchandise')
    list_filter = ('photoType', 'material_type', 'merchandise__consecutive_number')

admin.site.register(Foto, FotoAdmin)
admin.site.register(User)
admin.site.register(Merchandise)