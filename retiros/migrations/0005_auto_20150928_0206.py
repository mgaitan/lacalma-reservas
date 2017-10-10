# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retiros', '0004_auto_20150928_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='lugar_practica',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'\xc2\xbfPractica en algun centro de Yoga?', choices=[(b'baires', b'Sivananda Buenos Aires'), (b'montevideo', b'Sivananda Montevideo'), (b'neuquen', 'Sivananda Neuqu\xe9n'), (b'otro', b'Otro Centro de Yoga'), (b'ninguno', b'No asisto a ninguno')]),
        ),
    ]
