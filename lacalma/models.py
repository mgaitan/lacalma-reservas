from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
# Create your models here.
from datetime import date, timedelta


def dias_en_rango(inicio, fin):
    if fin < inicio:
        fin, inicio = inicio, fin
    dias = []
    for i in range((fin - inicio).days):
        dias.append(inicio + timedelta(days=i))
    return dias


TEMPORADA_ALTA = dias_en_rango(date(2014, 12, 27), date(2015, 2, 11))
TEMPORADA_MEDIA = dias_en_rango(date(2015, 2, 11), date(2015, 4, 6))  # hasta semana santa


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
    ESTADOS = Choices(('pendiente', 'confirmada'))
    departamento = models.ForeignKey('Departamento')
    desde = models.DateField()          # dia de entrada
    hasta = models.DateField()          # dia de salida
    nombre_y_apellido = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=50, help_text='Por favor, incluya la caracteristica')
    whatsapp = models.BooleanField('utiliza whatsapp', default=False)
    email = models.EmailField()
    estado = models.CharField(max_length=50, choices=ESTADOS, default=ESTADOS.pendiente)
    fecha_vencimiento_reserva = models.DateTimeField(null=True, blank=True)
    como_se_entero = models.TextField(null=True, blank=True)

    dias_baja = models.IntegerField(default=0)
    dias_media = models.IntegerField(default=0)
    dias_alta = models.IntegerField(default=0)
    costo_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def rango(self):
        return dias_en_rango(self.hasta, self.desde)

    def calcular(self):
        reserva = self.rango()
        self.dias_media = len(set(reserva).intersection(TEMPORADA_MEDIA))
        self.dias_alta = len(set(reserva).intersection(TEMPORADA_ALTA))
        self.dias_baja = len(reserva) - self.dias_media - self.dias_alta

        self.costo_total = sum((self.dias_media * self.departamento.dia_media,
                                self.dias_alta * self.departamento.dia_alta,
                                self.dias_baja * self.departamento.dia_baja,
                                ))

    def __str__(self):
        return "{departamento}: desde {desde} al {hasta} - {estado}".format(vars(self))
