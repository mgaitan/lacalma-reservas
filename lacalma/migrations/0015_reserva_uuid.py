# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0014_auto_20150124_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='uuid',
            field=models.CharField(max_length=8, null=True, editable=False),
            preserve_default=True,
        ),
    ]
