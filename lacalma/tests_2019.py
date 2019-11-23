from decimal import Decimal
from collections import OrderedDict

from django.test import TestCase
from django.utils.dateparse import parse_date as _
from .tests import ReservaFactory
from lacalma.models import Temporada, Departamento


class TestCase2019(TestCase):

    fixtures = ["deptos.json"]

    def setUp(self):
        self.depto = Departamento.objects.get(id=1)
        self.p0 = Temporada.objects.create(desde=_("2019-11-06"), hasta=_("2019-12-20"), nombre="p0", precio=3025)
        self.p1 = Temporada.objects.create(desde=_("2019-12-21"), hasta=_("2019-12-26"), nombre="p1", precio=3885)
        self.p2 = Temporada.objects.create(desde=_("2019-12-27"), hasta=_("2020-02-08"), nombre="p2", precio=5505)

        self.p0.departamentos.add(self.depto)
        self.p1.departamentos.add(self.depto)
        self.p2.departamentos.add(self.depto)

    def test_reserva(self):
        reserva = ReservaFactory(desde=_("2019-12-12"), hasta=_("2019-12-27"))
        reserva.save()
        assert reserva.costo_total == Decimal("50535.00")
        assert reserva.detalle() == OrderedDict(
            [
                (u"p0", (9, Decimal("3025.00"), Decimal("27225.00"))),
                (u"p1", (6, Decimal("3885.00"), Decimal("23310.00"))),
            ]
        )
