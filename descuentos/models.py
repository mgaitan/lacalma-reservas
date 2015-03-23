# -*- coding: utf-8 -*-
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices
from model_utils.fields import StatusField


class CodigoDeDescuento(TimeStampedModel):
    TIPOS_DESCUENTO = Choices(('porcentaje', 'Porcentaje'), ('monto_fijo', 'Monto fijo'))
    codigo = models.CharField(max_length=50, unique=True, help_text='Ejemplo: OTOÑO2015')
    tipo = models.CharField(max_length=50, choices=TIPOS_DESCUENTO, default=TIPOS_DESCUENTO.monto_fijo)
    monto = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        if self.tipo == CodigoDeDescuento.TIPOS_DESCUENTO.monto_fijo:
            return "%s - Descuento $ %s" % (self.codigo, self.monto)
        return "%s - Descuento %s%%" % (self.codigo, self.monto)

    def calcular_descuento(self, subtotal):
        if self.tipo == CodigoDeDescuento.TIPOS_DESCUENTO.monto_fijo:
            return self.monto
        else:
            return subtotal * self.monto / 100