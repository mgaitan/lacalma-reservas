# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0005_auto_20150928_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='antes',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo calificar\xc3\xada la atenci\xc3\xb3n previa a su reserva (consultas por email, facebook o tel\xc3\xa9fono)?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='calificacion',
            field=models.CharField(max_length=30, verbose_name=b'En general, \xc2\xbfC\xc3\xb3mo calificar\xc3\xada su estad\xc3\xada en La Calma?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='checking',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el checkin?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='checkout',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el checkout?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='limpieza',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo valorar\xc3\xada la limpieza al momento de ingresar?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='precio_calidad',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo valorar\xc3\xada la relaci\xc3\xb3n precio-calidad?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')]),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='proceso_reserva',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el proceso de reserva y pago de su estad\xc3\xada?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')]),
        ),
    ]
