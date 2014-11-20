# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_vencimiento_reserva',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
