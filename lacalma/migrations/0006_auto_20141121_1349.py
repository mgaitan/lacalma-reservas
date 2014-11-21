# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0005_auto_20141121_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='comentario',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='como_se_entero',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\xbfC\xf3mo conoci\xf3 La Calma?', choices=[(b'buscador', b'Por un buscador'), (b'facebook', b'Por Facebook'), (b'habitual', b'Ya alquil\xc3\xa9 anteriormente'), (b'recomendacion', 'Por una recomendaci\xf3n'), (b'inmobiliaria', 'Por la inmobiliaria'), (b'otro', b'Otro')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='procedencia',
            field=models.CharField(help_text=b'\xc2\xbfDe qu\xc3\xa9 ciudad nos visita?', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
