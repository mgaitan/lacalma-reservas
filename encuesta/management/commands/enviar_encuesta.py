# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # CommandError
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from lacalma.models import Reserva
from django.core.mail import send_mail
from django.contrib.sites.models import Site


site = Site.objects.get_current()
AHORA = timezone.now()


class Command(BaseCommand):
    help = """Envia un mail para pedir la encuesta"""

    def handle(self, *args, **options):
        for reserva in Reserva.objects.filter(estado=Reserva.ESTADOS.confirmada,
                                              hasta__lt=AHORA - timedelta(days=4),
                                              envio_encuesta__isnull=True):
            reserva.envio_encuesta = AHORA
            reserva.save(update_fields=['envio_encuesta'])

            mail_txt = render_to_string('mail_encuesta.txt', {'reserva': reserva, 'site': site})
            send_mail('La Calma - Encuesta de Satisfacción', mail_txt,
                'info@lacalma-lasgrutas.com.ar', [reserva.email])
