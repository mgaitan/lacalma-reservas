from django.contrib import admin
from lacalma.models import Departamento, Reserva


class DepartamentoAdmin(admin.ModelAdmin):
    pass


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'nombre_y_apellido', 'desde', 'hasta', 'estado', 'fecha_vencimiento_reserva')
    list_filter = ('departamento', 'estado', 'desde', 'hasta', 'fecha_vencimiento_reserva')
    search_fields = ('nombre_y_apellido', 'email')

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Reserva, ReservaAdmin)