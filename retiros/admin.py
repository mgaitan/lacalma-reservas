from django.contrib import admin
from .models import Inscripcion, Retiro


class RetiroAdmin(admin.ModelAdmin):
    def num(self, obj):
        return '#' + str(obj.id)

    list_display = ('num', 'nombre')



class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'retiro')
    list_filter = ('retiro',)
    search_fields = ('nombres', 'apellido' 'email')

admin.site.register(Retiro, RetiroAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)