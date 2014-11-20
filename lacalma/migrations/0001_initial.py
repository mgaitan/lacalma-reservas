# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
                ('capacidad', models.IntegerField()),
                ('dia_alta', models.DecimalField(max_digits=7, decimal_places=2)),
                ('dia_media', models.DecimalField(max_digits=7, decimal_places=2)),
                ('dia_baja', models.DecimalField(max_digits=7, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('desde', models.DateField()),
                ('hasta', models.DateField()),
                ('nombre_y_apellido', models.CharField(max_length=50)),
                ('procedencia', models.CharField(max_length=50, null=True, blank=True)),
                ('telefono', models.CharField(help_text=b'Por favor, incluya la caracteristica', max_length=50)),
                ('whatsapp', models.BooleanField(default=False, verbose_name=b'utiliza whatsapp')),
                ('email', models.EmailField(max_length=75)),
                ('estado', models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'confirmada')])),
                ('fecha_vencimiento_reserva', models.DateTimeField()),
                ('como_se_entero', models.TextField(null=True, blank=True)),
                ('dias_baja', models.IntegerField(default=0)),
                ('dias_media', models.IntegerField(default=0)),
                ('dias_alta', models.IntegerField(default=0)),
                ('costo_total', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('departamento', models.ForeignKey(to='lacalma.Departamento')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
