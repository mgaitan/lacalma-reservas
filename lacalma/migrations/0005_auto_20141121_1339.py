# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0004_auto_20141121_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='deposito_reserva',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserva',
            name='dias_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserva',
            name='fecha_deposito_reserva',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'pendiente'), (b'confirmada', b'confirmada'), (b'descartada', b'descartada')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='telefono',
            field=models.CharField(help_text='Por favor, incluya la caracter\xedstica', max_length=50),
            preserve_default=True,
        ),
    ]
