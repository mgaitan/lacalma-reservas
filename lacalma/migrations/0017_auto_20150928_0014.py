# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lacalma', '0016_reserva_envio_encuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='como_se_entero',
            field=models.CharField(blank=True, choices=[('buscador', 'Por un buscador'), ('facebook', 'Por Facebook'), ('habitual', 'Ya alquilé anteriormente'), ('recomendacion', 'Por una recomendación'), ('inmobiliaria', 'Por la inmobiliaria'), ('otro', 'Otro')], verbose_name='¿Cómo conoció La Calma?', null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='desde',
            field=models.DateField(verbose_name='Entra (14hs)'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, help_text='Por favor, revise atentamente que su dirección sea la correcta'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'pendiente'), ('confirmada', 'confirmada'), ('vencida', 'vencida'), ('cancelada', 'cancelada')], default='pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(choices=[('deposito', 'Depósito bancario'), ('mercadopago', 'Mercadopago')], verbose_name='Forma de pago', default='deposito', max_length=50),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='hasta',
            field=models.DateField(verbose_name='Sale (10hs)'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='mp_url',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='observaciones',
            field=models.TextField(blank=True, null=True, help_text='Se mostraran en el presupuesto o remito'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='procedencia',
            field=models.CharField(blank=True, max_length=50, null=True, help_text='¿De qué ciudad nos visita?'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='whatsapp',
            field=models.BooleanField(verbose_name='Utiliza whatsapp?', default=False),
        ),
    ]
