# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EncuestaSatisfaccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cocina', models.CharField(max_length=30, verbose_name='\xbfC\xf3mo valorar\xeda el equipamiento de cocina?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('living', models.CharField(max_length=30, verbose_name='\xbfC\xf3mo valorar\xeda el equipamiento del living comedor?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('banos', models.CharField(max_length=30, verbose_name='\xbfC\xf3mo valorar\xeda los ba\xf1os?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('habitaciones', models.CharField(max_length=30, verbose_name='\xbfC\xf3mo valorar\xeda las habitaciones?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('equipamiento_comentario', models.TextField(null=True, verbose_name='\xbfDe qu\xe9 manera podr\xedamos mejorar el confort del departamento?', blank=True)),
                ('limpieza', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo valorar\xc3\xada la limpieza al momento de ingresar?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('antes', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo calificar\xc3\xada la atenci\xc3\xb3n previa a su reserva (consultas por email, facebook o tel\xc3\xa9fono)?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('reserva', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el proceso de reserva y pago de su estad\xc3\xada?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')])),
                ('checking', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el checking?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')])),
                ('checkout', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo le result\xc3\xb3 el checkout?', choices=[(b'simple', b'simple'), (b'aceptable', b'aceptable'), (b'engorroso', b'engorroso')])),
                ('precio_calidad', models.CharField(max_length=30, verbose_name=b'\xc2\xbfC\xc3\xb3mo valorar\xc3\xada la relaci\xc3\xb3n precio-calidad?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('calificacion', models.CharField(max_length=30, verbose_name=b'En general, \xc2\xbfC\xc3\xb3mo calificar\xc3\xada su estad\xc3\xada en La Calma?', choices=[(b'malo', b'malo'), (b'regular', b'regular'), (b'bueno', b'bueno'), (b'muy bueno', b'muy bueno')])),
                ('comentario', models.TextField(null=True, verbose_name='\xbfTiene alg\xfan otro comentario u observaci\xf3n para hacernos?', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
