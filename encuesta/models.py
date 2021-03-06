# -*- coding: utf-8 -*-
from django.db import models
from lacalma.models import Reserva
from model_utils import Choices


class EncuestaSatisfaccion(models.Model):
    OPCIONES_BASE = Choices('malo', 'regular', 'bueno', 'muy bueno')
    OPCIONES_GRADO = Choices('simple', 'aceptable', 'engorroso')

    reserva_relacionada = models.ForeignKey('lacalma.Reserva', editable=False, related_name='encuesta')

    cocina = models.CharField(max_length=30, choices=OPCIONES_BASE,
                              verbose_name=u'¿Cómo valoraría el equipamiento de cocina?')
    living = models.CharField(max_length=30, choices=OPCIONES_BASE,
                              verbose_name=u'¿Cómo valoraría el equipamiento del living comedor?')
    banos = models.CharField(max_length=30, choices=OPCIONES_BASE,
                             verbose_name=u'¿Cómo valoraría los baños?')
    habitaciones = models.CharField(max_length=30, choices=OPCIONES_BASE,
                                    verbose_name=u'¿Cómo valoraría las habitaciones?')

    equipamiento_comentario = models.TextField(u'¿De qué manera podríamos mejorar el confort del departamento?',
                                               null=True, blank=True)

    limpieza = models.CharField(max_length=30, choices=OPCIONES_BASE,
                                verbose_name='¿Cómo valoraría la limpieza al momento de ingresar?')

    antes = models.CharField(max_length=30, choices=OPCIONES_BASE,
                               verbose_name='¿Cómo calificaría la atención previa a su reserva (consultas por email, facebook o teléfono)?')

    proceso_reserva = models.CharField(max_length=30, choices=OPCIONES_GRADO,
                               verbose_name='¿Cómo le resultó el proceso de reserva y pago de su estadía?')

    checking = models.CharField(max_length=30, choices=OPCIONES_GRADO,
                                verbose_name='¿Cómo le resultó el checkin?')

    checkout = models.CharField(max_length=30, choices=OPCIONES_GRADO,
                                verbose_name='¿Cómo le resultó el checkout?')

    precio_calidad = models.CharField(max_length=30, choices=OPCIONES_BASE,
                                      verbose_name='¿Cómo valoraría la relación precio-calidad?')

    calificacion = models.CharField(max_length=30, choices=OPCIONES_BASE,
                                    verbose_name='En general, ¿Cómo calificaría su estadía en La Calma?')

    comentario = models.TextField(verbose_name=u'¿Tiene algún otro comentario u observación para hacernos?',
                                  null=True, blank=True)

