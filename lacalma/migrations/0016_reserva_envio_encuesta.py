# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0015_reserva_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='envio_encuesta',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
