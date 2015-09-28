# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigodedescuento',
            name='codigo',
            field=models.CharField(max_length=50, unique=True, help_text='Ejemplo: OTOÑO2015'),
        ),
        migrations.AlterField(
            model_name='codigodedescuento',
            name='tipo',
            field=models.CharField(choices=[('porcentaje', 'Porcentaje'), ('monto_fijo', 'Monto fijo')], default='monto_fijo', max_length=50),
        ),
    ]
