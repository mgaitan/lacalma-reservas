from datetime import date, timedelta
from django.utils import timezone
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from lacalma.models import Reserva, Departamento, TEMPORADA_MEDIA, TEMPORADA_ALTA
from lacalma.forms import ReservaForm



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


class TestValidar(TestCase):

    fixtures = ['deptos.json']

    def test_comienza_entre_reserva(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        form = ReservaForm({'fechas': '23-11-2014 al 27-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'fechas': [u'Hay reservas realizadas durante esas fechas']})

    def test_comienza_mismo_dia_fin_anterior(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm({'fechas': '24-11-2014 al 27-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertTrue(form.is_valid())

    def test_termina_despues_de_reserva_previa(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm({'fechas': '10-11-2014 al 21-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'fechas': [u'Hay reservas realizadas durante esas fechas']})

    def test_termina_dia_reserva(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm({'fechas': '10-11-2014 al 19-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertTrue(form.is_valid())

    def test_solapamiento_total(self):
        ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30)).save()
        form = ReservaForm({'fechas': '10-11-2014 al 29-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'fechas': [u'Hay reservas realizadas durante esas fechas']})


    def test_ignora_vencidas(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = 'vencida'
        reserva.save()
        form = ReservaForm({'fechas': '10-11-2014 al 29-11-2014',
            'procedencia': None,
             'nombre_y_apellido': 'tin',
             'departamento': 1,
             'como_se_entero': None,
             'telefono': '33',
             'email': 'gaitan@gmail.com'})
        self.assertTrue(form.is_valid())


class TestVencidas(TestCase):

    fixtures = ['deptos.json']

    def test_simple_vencida(self):
        reserva1 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva1.fecha_vencimiento_reserva = timezone.now() - timedelta(days=1)
        reserva2 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30), depto=2)
        reserva2.fecha_vencimiento_reserva = timezone.now() + timedelta(days=1)

        reserva3 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30), depto=3)
        reserva3.fecha_vencimiento_reserva = timezone.now() - timedelta(days=1)     # vencidaza
        reserva3.estado = Reserva.ESTADOS.confirmada

        reserva1.save()
        reserva2.save()
        reserva3.save()
        call_command('limpiar_reservas')
        self.assertEqual(Reserva.objects.get(id=reserva1.id).estado, Reserva.ESTADOS.vencida)
        self.assertEqual(Reserva.objects.get(id=reserva2.id).estado, Reserva.ESTADOS.pendiente)
        self.assertEqual(Reserva.objects.get(id=reserva3.id).estado, Reserva.ESTADOS.confirmada)