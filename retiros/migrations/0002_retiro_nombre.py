# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retiros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retiro',
            name='nombre',
            field=models.CharField(default='retiro', help_text=b'Ejemplo: Vacaciones de Yoga Bariloche 2015', max_length=100),
            preserve_default=False,
        ),
    ]
