# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # CommandError
from django.utils import timezone
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

