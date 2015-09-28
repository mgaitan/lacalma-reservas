# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from lacalma.forms import ReservaAdminForm
from lacalma.models import Departamento, Reserva, ConceptoFacturable

site = '' # Site.objects.get_current()


class DepartamentoAdmin(admin.ModelAdmin):
    pass

class FacturableInline(admin.TabularInline):
    model = ConceptoFacturable


class ReservaAdmin(admin.ModelAdmin):

    def num(self, obj):
        return '#' + str(obj.id)

    def depto(self, obj):
        return obj.departamento.nombre

    depto.short_description = 'Departamento'

    def links(self, obj):
        return '<a href="http://%s%s" target="_blank">ver %s</a>' % (site.domain,
                                          reverse('presupuesto', args=(obj.id,)),
                                          'remito' if obj.estado == 'confirmada' else 'prespuesto')

    links.allow_tags = True
    links.short_description = 'Acciones'

    list_display = ('num', 'depto', 'nombre_y_apellido', 'desde', 'hasta', 'estado', 'fecha_vencimiento_reserva', 'forma_pago', 'links')
    list_filter = ('departamento', 'estado', 'desde', 'hasta', 'fecha_vencimiento_reserva', 'forma_pago')
    search_fields = ('nombre_y_apellido', 'email')
    readonly_fields = ('dias_alta', 'dias_baja', 'dias_media', 'dias_total', 'total_sin_descuento', 'costo_total')

    inlines = [
        FacturableInline,
    ]

    fieldsets = (
        ('Reserva', {
            'fields': ('departamento', 'desde', 'hasta', 'estado', 'mp_id')
        }),
        ('Vencimiento', {
            'fields': ('fecha_vencimiento_reserva',)
        }),
        ('Datos del cliente', {
            'fields': ('nombre_y_apellido', 'procedencia', 'email', 'telefono', 'whatsapp', )
        }),
        (u'Otra información', {
            'fields': ('como_se_entero', 'comentario', 'observaciones')
        }),
        ('Deposito', {
            'fields': ('deposito_reserva', 'fecha_deposito_reserva'),
        }),
        ('Dias y costos (se calcula automáticamente)', {
            'fields': ('dias_alta', 'dias_baja', 'dias_media', 'dias_total', 'costo_total')
        }),
    )

    def save_related(self, request, form, formsets, change):
        super(ReservaAdmin, self).save_related(request, form, formsets, change)
        form.instance.save()


admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Reserva, ReservaAdmin)