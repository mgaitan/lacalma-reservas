from datetime import date
import json
from django.shortcuts import render
from django.views.generic.edit import FormView
from lacalma.models import Reserva, Departamento
from lacalma.forms import ReservaForm



class ReservaView(FormView):
    template_name = 'index.html'
    form_class = ReservaForm


    def get_context_data(self, **kwargs):
        context = super(ReservaView, self).get_context_data(**kwargs)
        hoy = date.today()
        context['hoy'] = str(hoy)

        reservas_pendientes = {}
        reservas_confirmadas = {}
        for depto in Departamento.objects.all():
            pendientes = []
            confirmadas = []
            for reserva in Reserva.objects.filter(departamento=depto, desde__gte=hoy, estado=Reserva.ESTADOS.pendiente):
                pendientes.extend((d.isoformat() for d in reserva.rango()))
            for reserva in Reserva.objects.filter(departamento=depto, desde__gte=hoy, estado='confirmada'):
                confirmadas.extend((d.isoformat() for d in reserva.rango()))

            reservas_pendientes[str(depto.id)] = pendientes
            reservas_confirmadas[str(depto.id)] = confirmadas
        context['reservas_pendientes'] = json.dumps(reservas_pendientes)
        context['reservas_confirmadas'] = json.dumps(reservas_confirmadas)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        instance = form.save()
        return render(self.context, 'gracias.html', {})



