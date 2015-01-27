# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from model_utils import Choices
from model_utils.models import TimeStampedModel
from decimal import Decimal
from pytz import UTC
from django.utils import timezone
import uuid
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
    ESTADOS = Choices('pendiente', 'confirmada', 'vencida', 'cancelada')
    ENTERO = Choices(('buscador', 'Por un buscador'),
                     ('facebook', 'Por Facebook'),
                     ('habitual', 'Ya alquilé anteriormente'),
                     ('recomendacion', u'Por una recomendación'),
                     ('inmobiliaria', u'Por la inmobiliaria'),
                     ('otro', 'Otro'),)
    METODO = Choices(('deposito', u'Depósito bancario'), ('mercadopago', 'Mercadopago'))

    departamento = models.ForeignKey(Departamento)
    desde = models.DateField(verbose_name="Entra (14hs)")          # dia de entrada desde las 14hs
    hasta = models.DateField(verbose_name="Sale (10hs)")          # dia de salida hasta las 10hs
    nombre_y_apellido = models.CharField(max_length=50, null=True, blank=True)
    procedencia = models.CharField(max_length=50, null=True, blank=True, help_text='¿De qué ciudad nos visita?')
    telefono = models.CharField(max_length=50, null=True, blank=True, help_text=u'Por favor, incluya la característica')
    whatsapp = models.BooleanField('Utiliza whatsapp?', default=False)
    email = models.EmailField(null=True, blank=True, help_text="Por favor, revise atentamente que su dirección sea la correcta")
    estado = models.CharField(max_length=50, choices=ESTADOS, default=ESTADOS.pendiente)
    como_se_entero = models.CharField(verbose_name=u'¿Cómo conoció La Calma?', max_length=50, choices=ENTERO, null=True, blank=True)
    comentario = models.TextField(verbose_name=u'¿Algún comentario?', null=True, blank=True)
    forma_pago = models.CharField(verbose_name='Forma de pago', max_length=50, choices=METODO, default=METODO.deposito)


    dias_total = models.IntegerField(default=0)
    dias_baja = models.IntegerField(default=0)
    dias_media = models.IntegerField(default=0)
    dias_alta = models.IntegerField(default=0)

    costo_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    fecha_vencimiento_reserva = models.DateTimeField(null=True, blank=True)

    fecha_deposito_reserva = models.DateTimeField(null=True, blank=True)
    deposito_reserva = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    mp_id = models.CharField(verbose_name=u'ID Transacción de Mercadopago', max_length=100, null=True, blank=True)
    mp_pendiente = models.BooleanField(default=False)
    mp_url = models.CharField(max_length=255, default='')
    observaciones = models.TextField(help_text="Se mostraran en el presupuesto o remito", null=True, blank=True)
    uuid = models.CharField(max_length=8, null=True, editable=False)
    envio_encuesta = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Reserva #%s' % self.id

    def rango(self):
        return dias_en_rango(self.hasta, self.desde)

    def descuento(self):
        if self.dias_total >= 15:
            return DESCUENTO_QUINCENA, self.total_sin_descuento() * Decimal(str(DESCUENTO_QUINCENA / 100.0))
        else:
            return 0, 0

    def deposito_requerido(self):
        return DEPOSITO_REQUERIDO, self.total_sin_descuento() * Decimal(str(DEPOSITO_REQUERIDO / 100.0))

    def detalle(self):
        return {'media': self.dias_media * self.departamento.dia_media,
                'alta': self.dias_alta * self.departamento.dia_alta,
                'baja': self.dias_baja * self.departamento.dia_baja}

    def total_sin_descuento(self):
        return sum((self.dias_media * self.departamento.dia_media,
                    self.dias_alta * self.departamento.dia_alta,
                    self.dias_baja * self.departamento.dia_baja))

    def calcular_costo(self, aplicar_descuento=False):
        reserva = self.rango()
        self.dias_total = len(reserva)
        self.dias_media = len(set(reserva).intersection(TEMPORADA_MEDIA))
        self.dias_alta = len(set(reserva).intersection(TEMPORADA_ALTA))
        self.dias_baja = self.dias_total - self.dias_media - self.dias_alta

        self.costo_total = self.total_sin_descuento()

        self.costo_total -= self.descuento()[1]

        for facturable in self.facturables.all():
            self.costo_total += facturable.monto

    def saldo(self):
        return self.costo_total - self.deposito_reserva

    def calcular_vencimiento(self):
        # fecha vencimiento
        desde = datetime.combine(self.desde, time(14, 0, tzinfo=UTC))
        faltan = int((desde - timezone.now()).total_seconds() / 3600)
        if faltan >= 240:
            # mas de 10 dias?
            self.fecha_vencimiento_reserva = timezone.now() + timedelta(hours=48)
        else:
            self.fecha_vencimiento_reserva = desde - timedelta(hours=faltan*0.75)

    def save(self, *args, **kwargs):
        self.calcular_costo()
        if not self.uuid:
            self.uuid = str(uuid.uuid1()).split('-')[0]
        super(Reserva, self).save(*args, **kwargs)


    @classmethod
    def fecha_libre(cls, departamento, desde, hasta, exclude=None):
        qs = Reserva.objects.filter(departamento=departamento).\
                           exclude(estado=Reserva.ESTADOS.vencida).\
                           exclude(estado=Reserva.ESTADOS.cancelada).filter(
                                  Q(desde__range=(desde, hasta - timedelta(days=1))) |
                                  Q(hasta__range=(desde + timedelta(days=1), hasta)) |
                                  Q(desde__lte=desde,hasta__gte=hasta))
        if exclude:
            qs = qs.exclude(id=exclude.id)

        return not qs.exists()


class ConceptoFacturable(TimeStampedModel):
    """para descuentos o cobrar conceptos especiales"""

    reserva = models.ForeignKey(Reserva, related_name='facturables')
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0)
