# -*- coding: utf-8 -*-
import json
import unittest
from datetime import date, timedelta, datetime, time
import pytz
from django.utils import timezone
from freezegun import freeze_time
from decimal import Decimal
import responses
from django.test import TestCase
from django.core.management import call_command
from django.utils.dateparse import parse_date
from lacalma.models import Reserva, Departamento, ConceptoFacturable, dias_en_rango, Temporada, Dolar
from lacalma.forms import ReservaForm1, ReservaForm2

from django.test.utils import captured_stdout


def ReservaFactory(desde, hasta, depto=1):
    departamento = Departamento.objects.get(pk=depto)
    return Reserva(
        departamento=departamento,
        desde=desde,
        hasta=hasta,
        nombre_y_apellido="tin",
        telefono="33",
        email="gaitan@gmail.com",
    )


TEMPORADA_ALTA = date(2019, 12, 26), date(2020, 2, 14)
TEMPORADA_MEDIA = date(2020, 2, 15), date(2020, 4, 4)  # hasta semana santa
DESCUENTO_QUINCENA = None  # porciento
DESCUENTO_PAGO_CONTADO = 5  # porciento
DEPOSITO_REQUERIDO = 50


class BaseTestCase(TestCase):

    fixtures = ["deptos.json"]

    def setUp(self):
        self.depto = Departamento.objects.get(id=1)
        self.alta = Temporada.objects.create(
            nombre="alta", desde=TEMPORADA_ALTA[0], hasta=TEMPORADA_ALTA[1], precio=100
        )
        self.media = Temporada.objects.create(
            nombre="media", desde=TEMPORADA_MEDIA[0], hasta=TEMPORADA_MEDIA[1], precio=80
        )
        self.alta.departamentos.add(self.depto)
        self.media.departamentos.add(self.depto)


class TestCalcular(BaseTestCase):
    def test_1_dias_dentro_temporada(self):
        desde = TEMPORADA_ALTA[0]
        hasta = desde + timedelta(days=1)
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, Decimal(100))

    def test_2_dias_fuera_temporada(self):
        desde = date(2019, 12, 26) - timedelta(days=3)
        hasta = desde + timedelta(days=2)
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular_costo(False)
        self.assertEqual(reserva.costo_total, 2 * self.depto.precio_fuera_temporada)

    def test_entre_temporadas(self):
        desde = TEMPORADA_ALTA[1] - timedelta(days=2)  # 3 dias de alta
        hasta = TEMPORADA_MEDIA[0] + timedelta(days=4)  # 4 dias de media
        reserva = ReservaFactory(desde=desde, hasta=hasta)
        reserva.calcular_costo(False)
        assert reserva.costo_total == 3 * Decimal(100) + 4 * Decimal(80)
        detalle = reserva.detalle()
        assert detalle.keys() == ["alta", "media"]
        assert detalle["alta"] == (3, Decimal("100.00"), Decimal("300.00"))
        assert detalle["media"] == (4, Decimal("80.00"), Decimal("320.00"))


class TestValidar(BaseTestCase):

    fixtures = ["deptos.json"]

    def test_comienza_entre_reserva(self):
        ReservaFactory(desde=date(2015, 11, 20), hasta=date(2015, 11, 24)).save()
        form = ReservaForm1({"fechas": "23/11/2015 al 27/11/2015", "departamento": 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form._errors, {"__all__": [u"Hay reservas realizadas durante esas fechas para este departamento"]}
        )

    def test_comienza_mismo_dia_fin_anterior(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({"fechas": "24/11/2014 al 27/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())

    def test_termina_despues_de_reserva_previa(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({"fechas": "10/11/2014 al 21/11/2014", "departamento": 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form._errors, {"__all__": [u"Hay reservas realizadas durante esas fechas para este departamento"]}
        )

    def test_termina_dia_reserva(self):
        ReservaFactory(desde=date(2014, 11, 20), hasta=date(2014, 11, 24)).save()
        # entra el mismo dia
        form = ReservaForm1({"fechas": "10/11/2014 al 19/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())

    def test_solapamiento_total(self):
        ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30)).save()
        form = ReservaForm1({"fechas": "10/11/2014 al 29/11/2014", "departamento": 1})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form._errors, {"__all__": [u"Hay reservas realizadas durante esas fechas para este departamento"]}
        )

    def test_ignora_vencidas(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = "vencida"
        reserva.save()
        form = ReservaForm1({"fechas": "10/11/2014 al 29/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())

    def test_ignora_canceladas(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = "cancelada"
        reserva.save()
        form = ReservaForm1({"fechas": "10/11/2014 al 29/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())

    def test_mercadopago_vencida(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = "mercadopago"
        reserva.estado = "vencida"
        reserva.save()
        form = ReservaForm1({"fechas": "10/11/2014 al 29/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())

    def test_mercadopago_cancelada(self):
        reserva = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva.estado = "mercadopago"
        reserva.estado = "cancelada"
        reserva.save()
        form = ReservaForm1({"fechas": "10/11/2014 al 29/11/2014", "departamento": 1})
        self.assertTrue(form.is_valid())


class TestForm2(TestCase):
    def test_validar_emails_falla(self):
        form = ReservaForm2(data={"email": "gaitan@gmail.com", "email_confirma": "otro@gimail.com"})
        form.is_valid()
        self.assertEqual(form._errors["email"], ["Las direcciones no coinciden"])

    def test_validar_emails_coinciden(self):
        form = ReservaForm2(data={"email": "gaitan@gmail.com", "email_confirma": "gaitan@gmail.com"})
        form.is_valid()
        self.assertNotIn("email", form._errors)


class TestLimpiar(BaseTestCase):

    fixtures = ["deptos.json"]

    def test_simple_vencida(self):
        reserva1 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30))
        reserva1.fecha_vencimiento_reserva = timezone.now() - timedelta(days=1)
        reserva2 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30), depto=2)
        reserva2.fecha_vencimiento_reserva = timezone.now() + timedelta(days=1)

        reserva3 = ReservaFactory(desde=date(2014, 11, 1), hasta=date(2014, 11, 30), depto=3)
        reserva3.fecha_vencimiento_reserva = timezone.now() - timedelta(days=1)  # vencidaza
        reserva3.estado = Reserva.ESTADOS.confirmada

        reserva1.save()
        reserva2.save()
        reserva3.save()
        call_command("limpiar_reservas")
        self.assertEqual(Reserva.objects.get(id=reserva1.id).estado, Reserva.ESTADOS.vencida)
        self.assertEqual(Reserva.objects.get(id=reserva2.id).estado, Reserva.ESTADOS.pendiente)
        self.assertEqual(Reserva.objects.get(id=reserva3.id).estado, Reserva.ESTADOS.confirmada)

    def test_mp_fallo_envia_mail(self):
        from django.core.mail import outbox

        reserva1 = ReservaFactory(desde=TEMPORADA_ALTA[0], hasta=TEMPORADA_ALTA[0] + timedelta(days=10))
        reserva1.fecha_vencimiento_reserva = timezone.now() + timedelta(days=1)
        reserva1.forma_pago = Reserva.METODO.mercadopago
        reserva1.created = timezone.now() - timedelta(hours=2.1)
        assert reserva1.estado == Reserva.ESTADOS.pendiente
        assert not reserva1.mp_pendiente
        assert len(outbox) == 0
        reserva1.save()
        call_command("limpiar_reservas")
        reserva1 = Reserva.objects.get(id=reserva1.id)
        self.assertEqual(reserva1.estado, Reserva.ESTADOS.pendiente)
        # self.assertTrue(reserva1.mp_pendiente)
        self.assertEqual(len(outbox), 1)
        mail = outbox[0]
        self.assertTrue(mail.body.startswith("Estimado/a"))


class TestFacturables(BaseTestCase):
    @unittest.skip("Descuento desactivado")
    def test_descuento_pago_contado(self):
        PRECIO_DIA = self.alta.precio
        llega = TEMPORADA_ALTA[0]
        sale = llega + timedelta(days=15)
        reserva = ReservaFactory(desde=llega, hasta=sale)
        reserva.calcular_costo()  # con descuento
        self.assertEqual(reserva.dias_total, 15)
        self.assertEqual(reserva.descuento()[0], 5)
        self.assertEqual(reserva.total_sin_descuento(), Decimal(PRECIO_DIA * 15))
        self.assertEqual(reserva.descuento()[1], Decimal(PRECIO_DIA * 15) * Decimal("0.05"))
        self.assertEqual(reserva.costo_total, Decimal(PRECIO_DIA * 15) * Decimal("0.95"))

    def test_descuento_especial(self):
        PRECIO_DIA = self.alta.precio
        llega = TEMPORADA_ALTA[0]
        sale = llega + timedelta(days=2)
        reserva = ReservaFactory(desde=llega, hasta=sale)
        reserva.save()
        ConceptoFacturable(reserva=reserva, concepto="descuento especial 15%", monto="-10").save()
        reserva.calcular_costo(False)
        self.assertEqual(reserva.total_sin_descuento(), Decimal(PRECIO_DIA * 2))
        self.assertEqual(reserva.costo_total, Decimal(PRECIO_DIA * 2) - Decimal("10"))


class TestDiasOcupadosEnFrontEnd(TestCase):

    fixtures = ["deptos.json"]

    def test_pendiente_proximo_simple(self):
        maniana = date.today() + timedelta(days=1)
        rango = [(maniana + timedelta(days=i)) for i in range(5)]
        ReservaFactory(desde=rango[0], hasta=rango[-1]).save()
        response = self.client.get("/")
        fechas = json.loads(response.context["reservas_pendientes"])["1"]
        self.assertEqual(fechas, [d.isoformat() for d in rango[:-1]])

    def test_confirmada_en_curso(self):
        ayer = date.today() + timedelta(days=-1)
        rango = [(ayer + timedelta(days=i)) for i in range(5)]
        r = ReservaFactory(desde=rango[0], hasta=rango[-1])
        r.estado = Reserva.ESTADOS.confirmada
        r.save()
        response = self.client.get("/")
        fechas = json.loads(response.context["reservas_confirmadas"])["1"]
        self.assertEqual(fechas, [d.isoformat() for d in rango[:-1]])


class TestCalcularVencimiento(BaseTestCase):
    def test_vencimiento_mas_de_10_dias(self):
        desde = TEMPORADA_ALTA[0]
        hasta = TEMPORADA_ALTA[0] + timedelta(days=4)  # 4 dias de alta

        reserva = ReservaFactory(desde=desde, hasta=hasta)
        midnight = time(0, 0, tzinfo=pytz.utc)
        reserva_datetime = datetime.combine(TEMPORADA_ALTA[0] - timedelta(11), midnight)

        with freeze_time(reserva_datetime):  # mas de 10 dias vence a las 24hs.
            reserva.calcular_vencimiento()
        self.assertEqual(reserva.fecha_vencimiento_reserva, reserva_datetime + timedelta(hours=24))


class TestCambioPrecio(BaseTestCase):
    def setUp(self):
        super(TestCambioPrecio, self).setUp()

    def test_vigente(self):
        Dolar.objects.create(fecha=parse_date("2019-10-03"), precio="60.23")
        Dolar.objects.create(fecha=parse_date("2019-10-11"), precio="60.31")
        assert Dolar.vigente() == Decimal("60.31")

    @responses.activate
    def test_primer_precio(self):
        responses.add(
            responses.GET,
            "https://api.estadisticasbcra.com/usd_of_minorista",
            json=[{u"d": u"2019-10-10", u"v": 60.10}, {u"d": u"2019-10-11", u"v": 60.31}],
            status=200,
        )
        call_command("actualizar_precios")
        dolar = Dolar.objects.get()
        assert dolar.precio == Decimal("60.31")
        assert dolar.fecha == date(2019, 10, 11)

    @responses.activate
    def test_precio_sin_variacion(self):
        Dolar.objects.create(fecha=parse_date("2019-10-11"), precio=61)
        responses.add(
            responses.GET,
            "https://api.estadisticasbcra.com/usd_of_minorista",
            json=[{u"d": u"2019-10-10", u"v": 60}, {u"d": u"2019-10-11", u"v": 61}],
            status=200,
        )
        with captured_stdout() as stdout:
            call_command("actualizar_precios")
        assert stdout.getvalue() == "la variacion no supera 0.05\n"

    @responses.activate
    def test_precio_supera(self):
        original = self.alta.precio
        Dolar.objects.create(fecha=parse_date("2019-10-10"), precio=60)
        responses.add(
            responses.GET,
            "https://api.estadisticasbcra.com/usd_of_minorista",
            json=[{u"d": u"2019-10-10", u"v": 60}, {u"d": u"2019-10-11", u"v": 63.4}],
            status=200,
        )
        with captured_stdout() as stdout:
            call_command("actualizar_precios")

        assert Dolar.vigente() == Decimal("63.4")
        self.alta.refresh_from_db()
        from django.core.mail import outbox

        assert self.alta.precio == Decimal("110.00")
        assert len(outbox) == 1
        assert outbox[0].subject == "[La Calma] Cambio de precios"
        assert outbox[0].body.startswith(u"El dólar cambió un 5.67%\n\n")
        assert outbox[0].to == ['info@lacalma-lasgrutas.com.ar']
