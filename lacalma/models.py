# -*- coding: utf-8 -*-
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from decimal import Decimal
from django.utils import timezone
from datetime import datetime, date, timedelta, time


def dias_en_rango(inicio, fin):
    if fin < inicio:
        fin, inicio = inicio, fin
    dias = []
    for i in range((fin - inicio).days):
        dias.append(inicio + timedelta(days=i))
    return dias


TEMPORADA_ALTA = dias_en_rango(date(2014, 12, 27), date(2015, 2, 11))
TEMPORADA_MEDIA = dias_en_rango(date(2015, 2, 11), date(2015, 4, 6))  # hasta semana santa
DESCUENTO_QUINCENA = 10     # porciento
DEPOSITO_REQUERIDO = 50


class Departamento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    capacidad = models.IntegerField()
    dia_alta = models.DecimalField(max_digits=7, decimal_places=2)
    dia_media = models.DecimalField(max_digits=7, decimal_places=2)
    dia_baja = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return "%s (%s pax)" % (self.nombre, self.capacidad)


class Reserva(TimeStampedModel):
    ESTADOS = Choices('pendiente', 'confirmada', 'vencida')
    ENTERO = Choices(('buscador', 'Por un buscador'),
                     ('facebook', 'Por Facebook'),
                     ('habitual', 'Ya alquilé anteriormente'),
                     ('recomendacion', u'Por una recomendación'),
                     ('inmobiliaria', u'Por la inmobiliaria'),
                     ('otro', 'Otro'),)
    departamento = models.ForeignKey(Departamento)
    desde = models.DateField()          # dia de entrada desde las 14hs
    hasta = models.DateField()          # dia de salida hasta las 10hs
    nombre_y_apellido = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=50, null=True, blank=True, help_text='¿De qué ciudad nos visita?')
    telefono = models.CharField(max_length=50, help_text=u'Por favor, incluya la característica')
    whatsapp = models.BooleanField('utiliza whatsapp', default=False)
    email = models.EmailField()
    estado = models.CharField(max_length=50, choices=ESTADOS, default=ESTADOS.pendiente)
    como_se_entero = models.CharField(verbose_name=u'¿Cómo conoció La Calma?',  max_length=50, choices=ENTERO, null=True, blank=True)
    comentario = models.TextField(verbose_name=u'¿Algún comentario?', null=True, blank=True)

    dias_total = models.IntegerField(default=0)
    dias_baja = models.IntegerField(default=0)
    dias_media = models.IntegerField(default=0)
    dias_alta = models.IntegerField(default=0)

    costo_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    fecha_vencimiento_reserva = models.DateTimeField(null=True, blank=True)


    fecha_deposito_reserva = models.DateTimeField(null=True, blank=True)
    deposito_reserva = models.DecimalField(max_digits=7, decimal_places=2, default=0)


    def rango(self):
        return dias_en_rango(self.hasta, self.desde)

    def descuento(self):
        if self.dias_total >= 15:
            return DESCUENTO_QUINCENA, self.costo_total * Decimal(str(DESCUENTO_QUINCENA / 100.0))
        else:
            return 0, 0

    def deposito_requerido(self):
        return DEPOSITO_REQUERIDO, self.costo_total * Decimal(str(DEPOSITO_REQUERIDO / 100.0))


    def total_sin_descuento(self):
        return sum((self.dias_media * self.departamento.dia_media,
                    self.dias_alta * self.departamento.dia_alta,
                    self.dias_baja * self.departamento.dia_baja))


    def calcular(self, aplicar_descuento=False):
        reserva = self.rango()
        self.dias_total = len(reserva)
        self.dias_media = len(set(reserva).intersection(TEMPORADA_MEDIA))
        self.dias_alta = len(set(reserva).intersection(TEMPORADA_ALTA))
        self.dias_baja = self.dias_total - self.dias_media - self.dias_alta


        self.costo_total = sum((self.dias_media * self.departamento.dia_media,
                                self.dias_alta * self.departamento.dia_alta,
                                self.dias_baja * self.departamento.dia_baja,
                                ))

        self.costo_total -= self.descuento()[1]

        # fecha vencimiento
        desde = timezone.make_aware(datetime.combine(self.desde, time(14, 0)), timezone.get_current_timezone())
        faltan = int((desde - timezone.now()).total_seconds() / 3600)
        if faltan >= 240:
            # mas de 10 dias?
            self.fecha_vencimiento_reserva = timezone.now() + timedelta(hours=72)
        else:
            self.fecha_vencimiento_reserva = desde - timedelta(hours=faltan*0.75)