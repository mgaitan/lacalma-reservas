# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuestasatisfaccion',
            name='proceso_reserva',
            field=models.CharField(default='aceptable', max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el proceso de reserva y pago de su estad\xc3\xada?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')]),
            preserve_default=False,
        )
    ]
