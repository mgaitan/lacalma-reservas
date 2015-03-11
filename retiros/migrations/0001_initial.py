# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('estado', models.CharField(default=b'pendiente', max_length=50, choices=[(b'pendiente', b'pendiente'), (b'confirmada', b'confirmada'), (b'vencida', b'vencida'), (b'cancelada', b'cancelada')])),
                ('apellido', models.CharField(max_length=50)),
                ('nombres', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('documento', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50)),
                ('telefono', models.CharField(help_text=b'incluya el prefijo de su zona', max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('estado_civil', models.CharField(max_length=50, choices=[(b'soltero', b'soltero'), (b'casado', b'casado'), (b'divorciado', b'divorciado'), (b'viudo', b'viudo')])),
                ('enfermedades', models.TextField(null=True, blank=True)),
                ('medicamentos', models.TextField(null=True, blank=True)),
                ('contacto_emergencia', models.CharField(max_length=100)),
                ('telefono_emergencia', models.CharField(help_text=b'incluya el prefijo de su zona', max_length=100)),
                ('practica_desde', models.IntegerField(verbose_name='\xbfDesde qu\xe9 a\xf1o practica Yoga?', validators=[django.core.validators.MaxValueValidator(2015), django.core.validators.MinValueValidator(1950)])),
                ('lugar_practica', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'\xc2\xbfPractica en algun centro de Yoga?', choices=[(b'baires', b'Sivananda Buenos Aires'), (b'montevideo', b'Sivananda Montevideo'), (b'neuquen', 'Sivananda Neuqu\xe9n'), (b'otro', b'Otro Centro de Yoga'), (b'ninguno', b'No asisto a ninguno')])),
                ('medio_noticia', models.CharField(max_length=50, verbose_name='\xbfC\xf3mo se inform\xf3 de esta actividad?', choices=[(b'centro', 'A trav\xe9s de mi centro'), (b'web', b'Buscador/web'), (b'facebook', b'Facebook'), (b'email', 'Bolet\xedn/Email'), (b'contacto', 'A trav\xe9s un amigo/familiar'), (b'via_publica', 'V\xeda p\xfablica')])),
                ('comentario', models.TextField(null=True, verbose_name='Si desea, puede contarnos sus razones y expectativas para esta actividad', blank=True)),
                ('forma_pago', models.CharField(default=b'deposito', max_length=50, verbose_name=b'Forma de pago', choices=[(b'deposito', 'Dep\xf3sito bancario'), (b'mercadopago', b'Mercadopago')])),
                ('costo_total', models.DecimalField(max_digits=7, decimal_places=2)),
                ('fecha_vencimiento_reserva', models.DateTimeField(null=True, blank=True)),
                ('fecha_deposito_reserva', models.DateTimeField(null=True, blank=True)),
                ('deposito_reserva', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('mp_id', models.CharField(max_length=100, null=True, verbose_name='ID Transacci\xf3n de Mercadopago', blank=True)),
                ('mp_pendiente', models.BooleanField(default=False)),
                ('mp_url', models.CharField(default=b'', max_length=255)),
                ('observaciones', models.TextField(help_text=b'Se mostraran en el presupuesto o remito', null=True, blank=True)),
                ('uuid', models.CharField(max_length=8, null=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Retiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lugar', models.CharField(help_text=b'Nombre del complejo o lugar donde ser realiza', max_length=100)),
                ('ciudad', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono', models.CharField(max_length=100, null=True, blank=True)),
                ('cupo', models.IntegerField(null=True, blank=True)),
                ('inicio', models.DateTimeField()),
                ('fin', models.DateTimeField()),
                ('precio', models.DecimalField(max_digits=7, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='retiro',
            field=models.ForeignKey(to='retiros.Retiro'),
            preserve_default=True,
        ),
    ]
