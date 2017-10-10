# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0002_auto_20150928_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigodedescuento',
            name='codigo',
            field=models.CharField(help_text=b'Ejemplo: OTO\xc3\x91O2015', unique=True, max_length=50),
        ),
    ]
