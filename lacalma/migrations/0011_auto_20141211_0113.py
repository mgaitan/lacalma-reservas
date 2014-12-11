# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0010_auto_20141210_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(default=b'deposito', max_length=50, verbose_name=b'Forma de pago', choices=[(b'deposito', b'deposito'), (b'mercadopago', b'mercadopago')]),
            preserve_default=True,
        ),
    ]
