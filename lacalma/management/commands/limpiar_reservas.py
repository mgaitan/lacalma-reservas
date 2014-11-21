import os
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand  # CommandError
from datetime import datetime
from lacalma.models import Reserva


AHORA = datetime.now()


class Command(BaseCommand):
    help = """Marca vencidas reservas pendientes que superen la fecha de vencimiento"""

    def handle(self, *args, **options):
        for reserva in Reserva.objects.filter(estado=Reserva.ESTADOS.pendiente,
                                              fecha_vencimiento_reserva__lt=AHORA):
            reserva.estado = Reserva.ESTADOS.vencida
            reserva.save(update_fields=['estado'])