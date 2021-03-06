# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.contrib.sites.models import Site
from collections import OrderedDict
from model_utils import Choices
from model_utils.models import TimeStampedModel
from decimal import Decimal
from pytz import UTC
from django.utils import timezone
import uuid
from datetime import datetime, timedelta, time
import mercadopago



def aumento(alta_anterior, coef_aumento=1.35):
    """
    formula para calcular aumentos

        baja es 35% menos que alta
        media es 20% menos que alta
    """
    return [alta_anterior * coef_aumento * i for i in [.65, 0.8, 1]]


def dias_en_rango(inicio, fin, include_end=False):
    if fin < inicio:
        fin, inicio = inicio, fin
    dias = []
    extra = 1 if include_end else 0
    for i in range((fin - inicio).days + extra):
        dias.append(inicio + timedelta(days=i))
    return dias


DESCUENTO_QUINCENA = None     # porciento
DESCUENTO_PAGO_CONTADO = None    # porciento
DEPOSITO_REQUERIDO = 50


class Dolar(models.Model):
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=9, decimal_places=2)

    @classmethod
    def vigente(cls):
        first = cls.objects.order_by('-fecha').first()
        if first:
            return first.precio
    

class Temporada(models.Model):
    nombre = models.CharField(max_length=50)
    desde = models.DateField()
    hasta = models.DateField()
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    departamentos = models.ManyToManyField('Departamento', related_name='temporadas')


    def rango(self):
        return dias_en_rango(self.hasta, self.desde, True)

    def is_1_4(self):
        return self.departamentos.filter(nombre__in=["Departamento 1", "Departamento 4"]).count() == 2

    def is_2_3(self):
        return self.departamentos.filter(nombre__in=["Departamento 3", "Departamento 2"]).count() == 2

    def __str__(self):
        return "Desde %s hasta %s " % (self.desde, self.hasta)


class Departamento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    capacidad = models.IntegerField()
    precio_fuera_temporada = models.DecimalField(max_digits=9, decimal_places=2)

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
    forma_pago = models.CharField(verbose_name='Forma de pago', max_length=50, choices=METODO, default=METODO.deposito,
        help_text='Cambiarlo puede modificar el saldo a pagar por aplicar o quitar descuentos')

    dias_total = models.IntegerField(default=0)
    costo_total = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    fecha_vencimiento_reserva = models.DateTimeField(null=True, blank=True)

    fecha_deposito_reserva = models.DateTimeField(null=True, blank=True)
    deposito_reserva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    mp_id = models.CharField(verbose_name=u'ID Transacción de Mercadopago', max_length=100, null=True, blank=True)
    mp_pendiente = models.BooleanField(default=False)
    mp_url = models.CharField(verbose_name='Dirección p/Pago', max_length=255, default='', help_text='Puede copiar esta dirección para enviar por email u otro medio')
    observaciones = models.TextField(help_text="Se mostraran en el presupuesto o remito", null=True, blank=True)
    uuid = models.CharField(max_length=8, null=True, editable=False)
    envio_encuesta = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Reserva #%s' % self.id

    def rango(self):
        return dias_en_rango(self.hasta, self.desde)

    def descuento(self):
        if DESCUENTO_PAGO_CONTADO and self.forma_pago == Reserva.METODO.deposito:
            return DESCUENTO_PAGO_CONTADO, self.total_sin_descuento() * Decimal(str(DESCUENTO_PAGO_CONTADO / 100.0))
        else:
            return 0, 0

    def deposito_requerido(self):
        return DEPOSITO_REQUERIDO, self.total_sin_descuento() * Decimal(str(DEPOSITO_REQUERIDO / 100.0))

    def detalle(self):
        d = OrderedDict()
        reserva = self.rango()
        
        dias_en_temporada = 0
        for temporada in self.departamento.temporadas.filter(
            Q(desde__range=(self.desde, self.hasta)) |
            Q(hasta__range=(self.desde, self.hasta)) |
            Q(desde__lte=self.desde, hasta__gte=self.hasta)
        ):
            dias = len(set(reserva).intersection(set(temporada.rango())))
            if dias:
                d[temporada.nombre] = (dias, temporada.precio, dias * temporada.precio)
                dias_en_temporada += dias

        fuera_de_temporada = len(reserva) - dias_en_temporada
        if fuera_de_temporada:
            d['fuera de temporada'] = fuera_de_temporada, self.departamento.precio_fuera_temporada, fuera_de_temporada * self.departamento.precio_fuera_temporada
        return d

    def total_sin_descuento(self):
        return sum(i[2] for i in self.detalle().values())

    def calcular_costo(self, descuento=False):
        reserva = self.rango()
        self.dias_total = len(reserva)

        self.costo_total = self.total_sin_descuento()
        if descuento:
            self.costo_total -= self.descuento()[1]

        for facturable in self.facturables.all():
            self.costo_total += facturable.monto

    def saldo(self):
        return self.costo_total - self.deposito_reserva

    def calcular_vencimiento(self):
        # fecha vencimiento
        desde = datetime.combine(self.desde, time(14, 0, tzinfo=UTC))
        faltan = int((desde - timezone.now()).total_seconds() / 3600)
        if faltan >= 24*10:
            # faltan mas de 20 dias?
            self.fecha_vencimiento_reserva = timezone.now() + timedelta(hours=24)
        else:
            self.fecha_vencimiento_reserva = timezone.now() + timedelta(hours=24 - (240 - faltan)/24)

    def save(self, *args, **kwargs):
        self.calcular_costo()
        if not self.uuid:
            self.uuid = str(uuid.uuid1()).split('-')[0]
        super(Reserva, self).save(*args, **kwargs)

    def generar_cupon_mercadopago(self):
        """configura la reserva para ser pagada via mercadopago"""
        if self.forma_pago != Reserva.METODO.mercadopago:
            return
        site = Site.objects.get_current()
        mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)

        if self.mp_id and self.mp_pendiente:
            # TODO Log this.
            mp.cancel_payment(self.mp_id)

        # nuevo id
        self.mp_id = str(uuid.uuid1())

        title = "La Calma {}: {} al {} inclusive".format(self.departamento.nombre,
                                                         self.desde.strftime("%d/%m/%Y"),
                                                         (self.hasta - timedelta(days=1)).strftime("%d/%m/%Y"))
        if self.deposito_reserva:
            title += ' (saldo)'
        preference = mp.create_preference({
            "items": [
                {
                    "id": str(self.id),
                    "title": title,
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": float(self.saldo())
                }
            ],
            "payer": {
                "name": self.nombre_y_apellido,
                "email": self.email,
            },
            "back_urls": {
                "success": site.domain + reverse('gracias_mp'),
            },
            "auto_return": "approved",
            "external_reference": self.mp_id,
            "notification_url": site.domain + reverse('ipn'),
        })

        if settings.MP_SANDBOX_MODE:
            url = preference['response']['sandbox_init_point']
        else:
            url = preference['response']['init_point']
        self.mp_url = url
        self.save(update_fields=['mp_id', 'mp_url'])

    @classmethod
    def fecha_libre(cls, departamento, desde, hasta, exclude=None):
        qs = Reserva.objects.filter(
            departamento=departamento
        ).exclude(
            estado=Reserva.ESTADOS.vencida
        ).exclude(
            estado=Reserva.ESTADOS.cancelada
        ).filter(
            Q(desde__range=(desde, hasta - timedelta(days=1))) |
            Q(hasta__range=(desde + timedelta(days=1), hasta)) |
            Q(desde__lte=desde, hasta__gte=hasta)
        )
        if exclude:
            qs = qs.exclude(id=exclude.id)

        return not qs.exists()


class ConceptoFacturable(TimeStampedModel):
    """para descuentos o cobrar conceptos especiales"""

    reserva = models.ForeignKey(Reserva, related_name='facturables')
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
