# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0006_auto_20141121_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='comentario',
            field=models.TextField(null=True, verbose_name='\xbfAlg\xfan comentario?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'pendiente'), (b'confirmada', b'confirmada'), (b'vencida', b'vencida')]),
            preserve_default=True,
        ),
    ]
