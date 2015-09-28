# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retiros', '0003_auto_20150312_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'pendiente'), ('confirmada', 'confirmada'), ('vencida', 'vencida'), ('cancelada', 'cancelada')], default='pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='estado_civil',
            field=models.CharField(choices=[('soltero', 'soltero'), ('casado', 'casado'), ('divorciado', 'divorciado'), ('viudo', 'viudo')], max_length=50),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='fecha_nacimiento',
            field=models.DateField(help_text='Ej: 22/03/82'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='forma_pago',
            field=models.CharField(choices=[('deposito', 'Depósito bancario'), ('mercadopago', 'Mercadopago')], verbose_name='Forma de pago', default='deposito', max_length=50),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='lugar_practica',
            field=models.CharField(blank=True, choices=[('baires', 'Sivananda Buenos Aires'), ('montevideo', 'Sivananda Montevideo'), ('neuquen', 'Sivananda Neuquén'), ('otro', 'Otro Centro de Yoga'), ('ninguno', 'No asisto a ninguno')], verbose_name='¿Practica en algun centro de Yoga?', null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='medio_noticia',
            field=models.CharField(choices=[('centro', 'A través de mi centro'), ('web', 'Buscador/web'), ('facebook', 'Facebook'), ('email', 'Boletín/Email'), ('contacto', 'A través un amigo/familiar'), ('via_publica', 'Vía pública')], verbose_name='¿Cómo se informó de esta actividad?', max_length=50),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='mp_url',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='observaciones',
            field=models.TextField(blank=True, null=True, help_text='Se mostraran en el presupuesto o remito'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='telefono',
            field=models.CharField(max_length=100, help_text='incluya el prefijo de su zona'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='telefono_emergencia',
            field=models.CharField(max_length=100, help_text='incluya el prefijo de su zona'),
        ),
        migrations.AlterField(
            model_name='retiro',
            name='lugar',
            field=models.CharField(max_length=100, help_text='Nombre del complejo o lugar donde ser realiza'),
        ),
        migrations.AlterField(
            model_name='retiro',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ejemplo: Vacaciones de Yoga Bariloche 2015'),
        ),
    ]
