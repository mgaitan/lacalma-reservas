import os
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand  # CommandError
from datetime import datetime
from lacalma.models import Reserva
from django.core.mail import send_mail


AHORA = datetime.now()


class Command(BaseCommand):
    help = """Marca vencidas reservas pendientes que superen la fecha de vencimiento"""

    def handle(self, *args, **options):
        for reserva in Reserva.objects.filter(estado=Reserva.ESTADOS.pendiente,
                                              fecha_vencimiento_reserva__lt=AHORA):
            reserva.estado = Reserva.ESTADOS.vencida
            reserva.save(update_fields=['estado'])

            send_mail('[La Calma] Reserva vencida ref #%s' % reserva.id, u"La reserva #%d se venció" % reserva.id,
                  'info@lacalma-lasgrutas.com.ar', ['gaitan@gmail.com', 'gracielamothe@gmail.com'])

