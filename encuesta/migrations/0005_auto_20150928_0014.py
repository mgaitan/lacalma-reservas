# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0004_auto_20150127_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='antes',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo calificaría la atención previa a su reserva (consultas por email, facebook o teléfono)?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='banos',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría los baños?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='calificacion',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='En general, ¿Cómo calificaría su estadía en La Calma?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='checking',
            field=models.CharField(choices=[('simple', 'simple'), ('aceptable', 'aceptable'), ('engorroso', 'engorroso')], verbose_name='¿Cómo le resultó el checkin?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='checkout',
            field=models.CharField(choices=[('simple', 'simple'), ('aceptable', 'aceptable'), ('engorroso', 'engorroso')], verbose_name='¿Cómo le resultó el checkout?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='cocina',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría el equipamiento de cocina?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='habitaciones',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría las habitaciones?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='limpieza',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría la limpieza al momento de ingresar?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='living',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría el equipamiento del living comedor?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='precio_calidad',
            field=models.CharField(choices=[('malo', 'malo'), ('regular', 'regular'), ('bueno', 'bueno'), ('muy bueno', 'muy bueno')], verbose_name='¿Cómo valoraría la relación precio-calidad?', max_length=30),
        ),
        migrations.AlterField(
            model_name='encuestasatisfaccion',
            name='proceso_reserva',
            field=models.CharField(choices=[('simple', 'simple'), ('aceptable', 'aceptable'), ('engorroso', 'engorroso')], verbose_name='¿Cómo le resultó el proceso de reserva y pago de su estadía?', max_length=30),
        ),
    ]
