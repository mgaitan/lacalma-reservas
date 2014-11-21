# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0003_auto_20141121_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'pendiente'), (b'confirmada', b'confirmada')]),
            preserve_default=True,
        ),
    ]
