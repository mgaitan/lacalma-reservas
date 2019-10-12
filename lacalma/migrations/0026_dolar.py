# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-12 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0025_auto_20181126_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dolar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
    ]
