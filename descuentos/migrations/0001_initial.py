# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoDeDescuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('codigo', models.CharField(help_text=b'Ejemplo: OTO\xc3\x91O2015', unique=True, max_length=50)),
                ('tipo', models.CharField(default=b'monto_fijo', max_length=50, choices=[(b'porcentaje', b'Porcentaje'), (b'monto_fijo', b'Monto fijo')])),
                ('monto', models.DecimalField(max_digits=7, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
