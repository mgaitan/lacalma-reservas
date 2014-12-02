from datetime import date
from decimal import Decimal
import json
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.contrib.formtools.preview import FormPreview
from django.core.mail import send_mail
from django.template import RequestContext
from lacalma.models import Reserva, Departamento
from lacalma.forms import ReservaForm



class ReservaViewWithPreview(FormPreview):
    form_template = preview_template = 'index.html'

    def get_context(self, request, form):
        context = super(ReservaViewWithPreview, self).get_context(request, form)
        hoy = date.today()
        context['hoy'] = str(hoy)

        reservas_pendientes = {}
        reservas_confirmadas = {}
        for depto in Departamento.objects.all():
            pendientes = []
            confirmadas = []
            for reserva in Reserva.objects.filter(departamento=depto, desde__gte=hoy, estado=Reserva.ESTADOS.pendiente):
                pendientes.extend((d.isoformat() for d in reserva.rango()))
            for reserva in Reserva.objects.filter(departamento=depto, desde__gte=hoy, estado=Reserva.ESTADOS.confirmada):
                confirmadas.extend((d.isoformat() for d in reserva.rango()))

            reservas_pendientes[str(depto.id)] = pendientes
            reservas_confirmadas[str(depto.id)] = confirmadas
        context['reservas_pendientes'] = json.dumps(reservas_pendientes)
        context['reservas_confirmadas'] = json.dumps(reservas_confirmadas)
        return context

    def process_preview(self, request, form, context):
        reserva = form.save(commit=False)
        reserva.calcular()
        context['reserva'] = reserva


    def post_post(self, request):
        "Validates the POST data. If valid, calls done(). Else, redisplays form."
        f = self.form(request.POST, auto_id=self.get_auto_id())
        if f.is_valid():
            if not self._check_security_hash(request.POST.get(self.unused_name('hash'), ''),
                                             request, f):
                return self.failed_hash(request)  # Security hash failed.
            return self.done(request, f.cleaned_data, f)
        else:
            return render_to_response(self.form_template,
                self.get_context(request, f),
                context_instance=RequestContext(request))

    def done(self, request, cleaned_data, form):
        reserva = form.save(commit=False)
        reserva.calcular()
        reserva.save()
        mail_txt = render_to_string('mail_txt.html', {'reserva': reserva})
        mail_html = render_to_string('mail.html', {'reserva': reserva})

        send_mail('Reserva en La Calma - Las Grutas /ref. #%s' % reserva.id, mail_txt,
                  'info@lacalma-lasgrutas.com.ar', [reserva.email],
                  bcc=['gaitan@gmail.com', 'gracielamothe@gmail.com'],
                  html_message=mail_html)

        # mail_admin = render_to_string('mail_admin_txt.html', {'reserva': reserva})

        # send_mail('[La Calma] Nueva Reserva - ref #%s' % reserva.id, mail_admin,
        #          'info@lacalma-lasgrutas.com.ar', ['gaitan@gmail.com', 'gracielamothe@gmail.com'])

        return redirect('/gracias/')


def gracias(request):
    return render(request, 'index.html', {'gracias': True})



reserva_view = ReservaViewWithPreview(ReservaForm)


"""
A futuro. la inmobiliaria manejaba su propio calendario de ubicacion.

http://sanmatiaspropiedades.com/api-v2/rentals/www_query_all

76251878  La Calma 1
76251879  La Calma 2
76251910  La Calma 3
76251909  La Calma 4
"""