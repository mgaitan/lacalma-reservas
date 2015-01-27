# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0015_reserva_uuid'),
        ('encuesta', '0002_auto_20150127_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encuestasatisfaccion',
            name='reserva',
        ),
        migrations.AddField(
            model_name='encuestasatisfaccion',
            name='reserva_relacionada',
            field=models.ForeignKey(related_name='encuesta', default=1, to='lacalma.Reserva'),
            preserve_default=False,
        ),
    ]
