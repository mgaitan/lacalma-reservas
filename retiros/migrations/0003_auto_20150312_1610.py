# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retiros', '0002_retiro_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='fecha_nacimiento',
            field=models.DateField(help_text=b'Ej: 22/03/82'),
            preserve_default=True,
        ),
    ]
