# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-06 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0021_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='mp_url',
            field=models.CharField(default=b'', help_text=b'Puede copiar esta direcci\xc3\xb3n para enviar por email u otro medio', max_length=255, verbose_name=b'Direcci\xc3\xb3n p/Pago'),
        ),
    ]
