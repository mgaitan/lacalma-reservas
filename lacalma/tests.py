from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase
from lacalma.models import Reserva, Departamento, TEMPORADA_MEDIA, TEMPORADA_ALTA


def ReservaFactory(desde, hasta, depto=1):
    departamento = Departamento.objects.get(pk=depto)
    return Reserva(departamento=departamento, desde=desde, hasta=hasta,
                   nombre_y_apellido='tin', telefono='33', email='gaitan@gmail.com')


class TestCalcular(TestCase):

    fixtures = ['deptos.json']

    def test_1_dias_temporada_baja(self):
        reserva = ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 21))
        reserva.calcular()
        self.assertEqual(reserva.costo_total,  1 * Decimal(890.00))

    def test_2_dias_temporada_baja(self):
        reserva = ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 22))
        reserva.calcular()
        self.assertEqual(reserva.costo_total,  2 * Decimal(890.00))

    def test_7_dias_temporada_media(self):
        reserva = ReservaFactory(desde=date(2015, 2, 11), hasta=date(2015, 2, 11) + timedelta(days=7))
        reserva.calcular()
        self.assertEqual(reserva.costo_total,  7 * Decimal(1070.00))
        self.assertEqual(reserva.dias_media, 7)

    def test_entre_baja_y_alta(self):
        desde = TEMPORADA_ALTA[0] - timedelta(days=3)   # 3 dias de baja
        hasta = TEMPORADA_ALTA[0] + timedelta(days=4)   # 4 dias de alta
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular()
        self.assertEqual(reserva.costo_total,  4 * Decimal(1400.00) + 3 * Decimal(890.00))
        self.assertEqual(reserva.dias_media, 0)
        self.assertEqual(reserva.dias_baja, 3)
        self.assertEqual(reserva.dias_alta, 4)

    def test_entre_alta_y_media(self):
        desde = date(2015, 2, 8)        #   3 dias alta
        hasta = date(2015, 2, 12)   # 1 dia media
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular()
        self.assertEqual(reserva.costo_total,  3 * Decimal(1400.00) + 1 * Decimal(1070.00))
        self.assertEqual(reserva.dias_media, 1)
        self.assertEqual(reserva.dias_baja, 0)
        self.assertEqual(reserva.dias_alta, 3)