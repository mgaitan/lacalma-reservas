# -*- coding: utf-8 -*-
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import uuid


CURRENT_YEAR = timezone.now().year


# Create your models here.

class Retiro(models.Model):
    nombre = models.CharField(max_length=100, help_text='Ejemplo: Vacaciones de Yoga Bariloche 2015')
    lugar = models.CharField(max_length=100, help_text='Nombre del complejo o lugar donde ser realiza')
    ciudad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    cupo = models.IntegerField(null=True, blank=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    precio = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return self.nombre


class Inscripcion(TimeStampedModel):
    ESTADOS = Choices('pendiente', 'confirmada', 'vencida', 'cancelada')

    ESTADO_CIVIL = Choices('soltero', 'casado', 'divorciado', 'viudo')
    CENTROS_YOGA = Choices(('baires', 'Sivananda Buenos Aires'),
                                ('montevideo', 'Sivananda Montevideo'),
                                ('neuquen', u'Sivananda Neuquén'),
                                ('otro', 'Otro Centro de Yoga'),
                                ('ninguno', 'No asisto a ninguno'))
    MEDIOS = Choices(('centro', u'A través de mi centro'), ('web', 'Buscador/web'),
                     ('facebook', 'Facebook'), ('email', u'Boletín/Email'), ('contacto', u'A través un amigo/familiar'),
                     ('via_publica', u'Vía pública'))
    METODO = Choices(('deposito', u'Depósito bancario'), ('mercadopago', 'Mercadopago'))

    estado = models.CharField(max_length=50, choices=ESTADOS, default=ESTADOS.pendiente)

    retiro = models.ForeignKey(Retiro)
    apellido = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    documento = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    telefono = models.CharField(max_length=100, help_text='incluya el prefijo de su zona')
    email = models.EmailField()
    estado_civil = models.CharField(max_length=50, choices=ESTADO_CIVIL)
    enfermedades = models.TextField(null=True, blank=True)
    medicamentos = models.TextField(null=True, blank=True)
    contacto_emergencia = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=100, help_text='incluya el prefijo de su zona')
    practica_desde = models.IntegerField(u'¿Desde qué año practica Yoga?', validators=[MaxValueValidator(CURRENT_YEAR), MinValueValidator(1950)])
    lugar_practica = models.CharField('¿Practica en algun centro de Yoga?', max_length=50, null=True, blank=True, choices=CENTROS_YOGA)
    medio_noticia = models.CharField(u'¿Cómo se informó de esta actividad?', max_length=50, choices=MEDIOS)

    comentario = models.TextField(u'Si desea, puede contarnos sus razones y expectativas para esta actividad', null=True, blank=True)

    forma_pago = models.CharField('Forma de pago', max_length=50, choices=METODO, default=METODO.deposito)

    costo_total = models.DecimalField(max_digits=7, decimal_places=2)

    fecha_vencimiento_reserva = models.DateTimeField(null=True, blank=True)

    fecha_deposito_reserva = models.DateTimeField(null=True, blank=True)
    deposito_reserva = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    mp_id = models.CharField(verbose_name=u'ID Transacción de Mercadopago', max_length=100, null=True, blank=True)
    mp_pendiente = models.BooleanField(default=False)
    mp_url = models.CharField(max_length=255, default='')
    observaciones = models.TextField(help_text="Se mostraran en el presupuesto o remito", null=True, blank=True)
    uuid = models.CharField(max_length=8, null=True, editable=False)

    def __unicode__(self):
        return u'Inscripcion #%s' % self.id


    @property
    def nombre_completo(self):
        return u"%s %s" % (self.nombres, self.apellido)

    def saldo(self):
        return self.costo_total - self.deposito_reserva

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid1()).split('-')[0]
        if not self.costo_total:
            self.costo_total = self.retiro.precio
        super(Inscripcion, self).save(*args, **kwargs)