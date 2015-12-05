# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0017_auto_20150928_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(choices=[('deposito', 'Depósito bancario'), ('mercadopago', 'Mercadopago')], default='deposito', help_text='Cambiarlo puede modificar el saldo a pagar por aplicar o quitar descuentos', max_length=50, verbose_name='Forma de pago'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='mp_url',
            field=models.CharField(default='', help_text='Puede copiar esta dirección para enviar por email u otro medio', max_length=255, verbose_name='Dirección p/Pago'),
        ),
    ]
