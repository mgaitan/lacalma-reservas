# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0012_reserva_observaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(default=b'deposito', max_length=50, verbose_name=b'Forma de pago', choices=[(b'deposito', 'Dep\xf3sito bancario'), (b'mercadopago', b'Mercadopago')]),
            preserve_default=True,
        ),
    ]
