# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # CommandError
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from lacalma.models import Reserva
from django.core.mail import send_mail

AHORA = timezone.now()


class Command(BaseCommand):
    help = """Marca vencidas reservas pendientes que superen la fecha de vencimiento"""

    def handle(self, *args, **options):
        for reserva in Reserva.objects.filter(estado=Reserva.ESTADOS.pendiente,
                                              fecha_vencimiento_reserva__lt=AHORA):
            reserva.estado = Reserva.ESTADOS.vencida
            reserva.save(update_fields=['estado'])
            mail_txt = render_to_string('mail_admin_vencio_txt.html', {'reserva': reserva})
            send_mail('[La Calma] Reserva vencida ref #%s' % reserva.id, mail_txt,
                'info@lacalma-lasgrutas.com.ar', ['info@lacalma-lasgrutas.com.ar'])

        for reserva in Reserva.objects.filter(estado=Reserva.ESTADOS.pendiente,
                                              forma_pago=Reserva.METODO.mercadopago,
                                              created__lt=AHORA - timedelta(hours=5)).\
                                              exclude(mp_pendiente=True):
            reserva.mp_pendiente = True
            reserva.save(update_fields=['mp_pendiente'])
            mail_txt = render_to_string('mail_mp.txt', {'reserva': reserva})
            send_mail('Sobre su reserva en Complejo La Calma (ref #%i)?' % reserva.id, mail_txt,
                reserva.email, ['info@lacalma-lasgrutas.com.ar'])
