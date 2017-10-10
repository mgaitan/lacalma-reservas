# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0019_auto_20151009_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(default=b'deposito', help_text=b'Cambiarlo puede modificar el saldo a pagar por aplicar o quitar descuentos', max_length=50, verbose_name=b'Forma de pago', choices=[(b'deposito', 'Dep\xf3sito bancario'), (b'mercadopago', b'Mercadopago')]),
        ),
    ]
