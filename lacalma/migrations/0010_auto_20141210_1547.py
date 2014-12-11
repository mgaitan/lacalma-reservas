# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0009_auto_20141209_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='mp_id',
            field=models.CharField(max_length=100, null=True, verbose_name='ID Transacci\xf3n de Mercadopago', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='email',
            field=models.EmailField(help_text=b'Por favor, revise atentamente que su direcci\xc3\xb3n sea la correcta', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
    ]
