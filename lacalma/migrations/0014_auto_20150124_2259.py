# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0013_auto_20141219_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='mp_pendiente',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserva',
            name='mp_url',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
