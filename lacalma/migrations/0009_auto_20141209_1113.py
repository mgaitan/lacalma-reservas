# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0008_auto_20141206_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(default=b'deposito', max_length=50, choices=[(b'deposito', b'deposito'), (b'mercadopago', b'mercadopago')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'pendiente'), (b'confirmada', b'confirmada'), (b'vencida', b'vencida'), (b'cancelada', b'cancelada')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='nombre_y_apellido',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='telefono',
            field=models.CharField(help_text='Por favor, incluya la caracter\xedstica', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='whatsapp',
            field=models.BooleanField(default=False, verbose_name=b'Utiliza whatsapp?'),
            preserve_default=True,
        ),
    ]
