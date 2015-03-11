from django.contrib import admin
from .models import Inscripcion, Retiro


class RetiroAdmin(admin.ModelAdmin):
    pass


class InscripcionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Retiro, RetiroAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)