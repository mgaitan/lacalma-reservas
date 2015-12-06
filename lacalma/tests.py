import json
from datetime import date, timedelta, datetime
import pytz
from django.utils import timezone
from freezegun import freeze_time
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from lacalma.models import Reserva, Departamento, TEMPORADA_ALTA, TEMPORADA_MEDIA, ConceptoFacturable
from lacalma.forms import ReservaForm1, ReservaForm2


def ReservaFactory(desde, hasta, depto=1):
    departamento = Departamento.objects.get(pk=depto)
    return Reserva(departamento=departamento, desde=desde, hasta=hasta,
                   nombre_y_apellido='tin', telefono='33', email='gaitan@gmail.com')

"""
TEMPORADA_ALTA = dias_en_rango(date(2015, 12, 26), date(2016, 2, 14))
TEMPORADA_MEDIA = dias_en_rango(date(2016, 2, 15), date(2016, 4, 4))  # hasta semana santa
DESCUENTO_QUINCENA = None     # porciento
DESCUENTO_PAGO_CONTADO = 5    # porciento
DEPOSITO_REQUERIDO = 50
"""

class TestCalcular(TestCase):

    fixtures = ['deptos.json']

    def test_1_dias_temporada_baja(self):
        reserva = ReservaFactory(desde=date(2015, 11, 20), hasta=date(2015, 11, 21))
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, Decimal(1230.00) )

    def test_2_dias_temporada_baja(self):
        reserva = ReservaFactory(desde=date(2015, 11, 20), hasta=date(2015, 11, 22))
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, 2 * Decimal(1230.00))

    def test_7_dias_temporada_media(self):
        reserva = ReservaFactory(desde=TEMPORADA_MEDIA[0], hasta=TEMPORADA_MEDIA[0] + timedelta(days=7))
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, 7 * Decimal(1520.00))
        self.assertEqual(reserva.dias_media, 7)

    def test_entre_baja_y_alta(self):
        desde = TEMPORADA_ALTA[0] - timedelta(days=3)   # 3 dias de baja
        hasta = TEMPORADA_ALTA[0] + timedelta(days=4)   # 4 dias de alta
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, 4 * Decimal(1900) + 3 * Decimal(1230.00))
        self.assertEqual(reserva.dias_media, 0)
        self.assertEqual(reserva.dias_baja, 3)
        self.assertEqual(reserva.dias_alta, 4)

    def test_entre_alta_y_media(self):

        desde = TEMPORADA_ALTA[-3]        #   3 dias alta
        hasta = TEMPORADA_MEDIA[1]        # 1 dia media
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular_costo(False)
        self.assertEqual(reserva.dias_media, 1)
        self.assertEqual(reserva.dias_baja, 0)
        self.assertEqual(reserva.dias_alta, 3)
        self.assertEqual(reserva.costo_total,  3 * Decimal(1900) + 1 * Decimal(1520.00))


class TestValidar(TestCase):

    fixtures = ['deptos.json']

    def test_comienza_entre_reserva(self):
        ReservaFactory(desde=date(2015, 11, 20), hasta=date(2015, 11, 24)).save()
        form = ReservaForm1({'fechas': '23/11/2015 al 27/11/2015', 'departamento': 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'__all__': [u'Hay reservas realizadas durante esas fechas para este departamento']})

    def test_comienza_mismo_dia_fin_anterior(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({'fechas': '24/11/2014 al 27/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())

    def test_termina_despues_de_reserva_previa(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({'fechas': '10/11/2014 al 21/11/2014',
             'departamento': 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'__all__': [u'Hay reservas realizadas durante esas fechas para este departamento']})

    def test_termina_dia_reserva(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({'fechas': '10/11/2014 al 19/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())

    def test_solapamiento_total(self):
        ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30)).save()
        form = ReservaForm1({'fechas': '10/11/2014 al 29/11/2014',
             'departamento': 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(form._errors, {'__all__': [u'Hay reservas realizadas durante esas fechas para este departamento']})

    def test_ignora_vencidas(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = 'vencida'
        reserva.save()
        form = ReservaForm1({'fechas': '10/11/2014 al 29/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())

    def test_ignora_canceladas(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = 'cancelada'
        reserva.save()
        form = ReservaForm1({'fechas': '10/11/2014 al 29/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())

    def test_mercadopago_vencida(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = 'mercadopago'
        reserva.estado = 'vencida'
        reserva.save()
        form = ReservaForm1({'fechas': '10/11/2014 al 29/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())

    def test_mercadopago_cancelada(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = 'mercadopago'
        reserva.estado = 'cancelada'
        reserva.save()
        form = ReservaForm1({'fechas': '10/11/2014 al 29/11/2014',
             'departamento': 1})
        self.assertTrue(form.is_valid())


class TestForm2(TestCase):

    def test_validar_emails_falla(self):
        form = ReservaForm2(data={'email': 'gaitan@gmail.com', 'email_confirma': 'otro@gimail.com'})
        form.is_valid()
        self.assertEqual(form._errors['email'], ['Las direcciones no coinciden'])

    def test_validar_emails_coinciden(self):
        form = ReservaForm2(data={'email': 'gaitan@gmail.com', 'email_confirma': 'gaitan@gmail.com'})
        form.is_valid()
        self.assertNotIn('email', form._errors)


class TestLimpiar(TestCase):

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

    def test_mp_fallo_envia_mail(self):
        from django.core.mail import outbox

        reserva1 = ReservaFactory(desde=TEMPORADA_ALTA[0], hasta=TEMPORADA_ALTA[10])
        reserva1.fecha_vencimiento_reserva = timezone.now() + timedelta(days=1)
        reserva1.forma_pago = Reserva.METODO.mercadopago
        reserva1.created = timezone.now() - timedelta(hours=2.1)
        assert reserva1.estado == Reserva.ESTADOS.pendiente
        assert not reserva1.mp_pendiente
        assert len(outbox) == 0
        reserva1.save()
        call_command('limpiar_reservas')
        reserva1 = Reserva.objects.get(id=reserva1.id)
        self.assertEqual(reserva1.estado, Reserva.ESTADOS.pendiente)
        # self.assertTrue(reserva1.mp_pendiente)
        self.assertEqual(len(outbox), 1)
        mail = outbox[0]
        self.assertTrue(mail.body.startswith('Estimado/a'))


class TestDescuento(TestCase):

    fixtures = ['deptos.json']

    def test_descuento(self):
        PRECIO_DIA = Departamento.objects.get(pk=1).dia_alta
        llega = TEMPORADA_ALTA[0]
        sale = llega + timedelta(days=15)
        reserva = ReservaFactory(desde=llega, hasta=sale)
        reserva.calcular_costo()  # con descuento
        self.assertEqual(reserva.dias_total, 15)
        self.assertEqual(reserva.descuento()[0], 5)
        self.assertEqual(reserva.total_sin_descuento(), Decimal(PRECIO_DIA * 15))
        self.assertEqual(reserva.descuento()[1], Decimal(PRECIO_DIA * 15) * Decimal('0.05'))
        self.assertEqual(reserva.costo_total, Decimal(PRECIO_DIA * 15) * Decimal('0.95'))


class TestFacturables(TestCase):

    fixtures = ['deptos.json']

    def test_descuento_especial(self):
        PRECIO_DIA = Departamento.objects.get(pk=1).dia_alta
        llega = TEMPORADA_ALTA[0]
        sale = llega + timedelta(days=2)
        reserva = ReservaFactory(desde=llega, hasta=sale)
        reserva.save()
        ConceptoFacturable(reserva=reserva, concepto='descuento especial 15%', monto='-10').save()
        reserva.calcular_costo(False)
        self.assertEqual(reserva.total_sin_descuento(), Decimal(PRECIO_DIA * 2))
        self.assertEqual(reserva.costo_total, Decimal(PRECIO_DIA * 2) - Decimal('10'))


class TestDiasOcupadosEnFrontEnd(TestCase):

    fixtures = ['deptos.json']

    def test_pendiente_proximo_simple(self):
        maniana = date.today() + timedelta(days=1)
        rango = [(maniana + timedelta(days=i)) for i in range(5)]
        ReservaFactory(desde=rango[0],
                       hasta=rango[-1]).save()
        response = self.client.get('/')
        fechas = json.loads(response.context['reservas_pendientes'])["1"]
        self.assertEqual(fechas, [d.isoformat() for d in rango[:-1]])


    def test_confirmada_en_curso(self):
        ayer = date.today() + timedelta(days=-1)
        rango = [(ayer + timedelta(days=i)) for i in range(5)]
        r = ReservaFactory(desde=rango[0],
                       hasta=rango[-1])
        r.estado = Reserva.ESTADOS.confirmada
        r.save()
        response = self.client.get('/')
        fechas = json.loads(response.context['reservas_confirmadas'])["1"]
        self.assertEqual(fechas, [d.isoformat() for d in rango[:-1]])


class TestCalcularVencimiento(TestCase):

    fixtures = ['deptos.json']

    def test_vencimiento_mas_de_10_dias(self):

        reserva = ReservaFactory(desde=date(2015, 12, 1), hasta=date(2015, 12, 5))

        with freeze_time("2015-11-20 12:00:00"):     # mas de 10 dias vence a las 24hs.
            reserva.calcular_vencimiento()
        self.assertEqual(reserva.fecha_vencimiento_reserva, datetime(2015,11,21,12,0,0,tzinfo=pytz.utc))


    def test_vencimiento_menos_de_10_dias(self):

        reserva = ReservaFactory(desde=date(2015, 12, 1), hasta=date(2015, 12, 5))

        with freeze_time("2015-11-22 12:00:00"):     # menos de 10 dias vence
            reserva.calcular_vencimiento()
            self.assertTrue(timedelta(hours=24) > reserva.fecha_vencimiento_reserva - timezone.now() > timedelta(hours=23))

