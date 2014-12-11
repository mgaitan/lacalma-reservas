# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0011_auto_20141211_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='observaciones',
            field=models.TextField(help_text=b'Se mostraran en el presupuesto o remito', null=True, blank=True),
            preserve_default=True,
        ),
    ]
