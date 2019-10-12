# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # CommandError
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import requests
from lacalma.models import Temporada, Dolar
from django.core.mail import send_mail
from django.utils.dateparse import parse_date


AHORA = timezone.now()
LIMITE = 0.05  # variacion del
HEADERS = {"Authorization": "BEARER {}".format(settings.BCRA_TOKEN)}


class Command(BaseCommand):
    help = """Actualiza precios de temporada si el dolar salta un porcentaje"""

    def handle(self, *args, **options):
        precio_vigente = Dolar.vigente()
        response = requests.get("https://api.estadisticasbcra.com/usd_of_minorista", headers=HEADERS)
        response.raise_for_status()
        fecha, precio_actual = response.json()[-1]["d"], response.json()[-1]["v"]
        if not precio_vigente:
            Dolar.objects.create(fecha=parse_date(fecha), precio=precio_actual)
            print("Se obtuvo primer precio de referencia {}".format(precio_actual))
        else:
            porcentaje_dif = (precio_actual - precio_vigente) / precio_vigente
            if abs(porcentaje_dif) > LIMITE:
                Dolar.objects.create(fecha=parse_date(fecha), precio=precio_actual)

                texto = []
                for t in Temporada.objects.all():
                    t.precio = t.precio * (1 + porcentaje_dif)
                    t.save(update_fields=["precio"])
                    texto.append(
                        "- Temporada {} - Depto {}: ${}".format(t.nombre, "1 o 4" if t.is_1_4 else "2 o 3", t.precio)
                    )

                # la diferencia de precio es grande
                send_mail(
                    "[La Calma] Cambio de precios",
                    "Los precios cambiaron un {}%\n\n{}".format(porcentaje_dif * 100, "\n".join(texto)),
                    "info@lacalma-lasgrutas.com.ar",
                    ["info@lacalma-lasgrutas.com.ar"],
                )
            else:
                print("la variacion no supera {}".format(LIMITE))
