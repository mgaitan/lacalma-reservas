# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0003_auto_20150127_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='checking',
            field=models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el checkin?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='reserva_relacionada',
            field=models.ForeignKey(related_name='encuesta', editable=False, to='lacalma.Reserva'),
            preserve_default=True,
        ),
    ]
