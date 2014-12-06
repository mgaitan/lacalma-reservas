# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0007_auto_20141202_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptoFacturable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('concepto', models.CharField(max_length=200)),
                ('monto', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('reserva', models.ForeignKey(related_name='facturables', to='lacalma.Reserva')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='desde',
            field=models.DateField(verbose_name=b'Entra (14hs)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reserva',
            name='hasta',
            field=models.DateField(verbose_name=b'Sale (10hs)'),
            preserve_default=True,
        ),
    ]
