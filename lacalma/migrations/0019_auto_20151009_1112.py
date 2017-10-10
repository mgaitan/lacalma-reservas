# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0018_auto_20150928_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='mp_url',
            field=models.CharField(default=b'', help_text=b'Puede copiar esta direcci\xc3\xb3n para enviar por email u otro medio', max_length=255, verbose_name=b'Direcci\xc3\xb3n p/Pago'),
        ),
    ]
