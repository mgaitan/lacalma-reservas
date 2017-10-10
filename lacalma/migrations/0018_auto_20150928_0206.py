# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0017_auto_20150928_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='como_se_entero',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\xbfC\xf3mo conoci\xf3 La Calma?', choices=[(b'buscador', b'Por un buscador'), (b'facebook', b'Por Facebook'), (b'habitual', b'Ya alquil\xc3\xa9 anteriormente'), (b'recomendacion', 'Por una recomendaci\xf3n'), (b'inmobiliaria', 'Por la inmobiliaria'), (b'otro', b'Otro')]),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='email',
            field=models.EmailField(help_text=b'Por favor, revise atentamente que su direcci\xc3\xb3n sea la correcta', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='procedencia',
            field=models.CharField(help_text=b'\xc2\xbfDe qu\xc3\xa9 ciudad nos visita?', max_length=50, null=True, blank=True),
        ),
    ]
