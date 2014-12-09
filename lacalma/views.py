from datetime import date, timedelta, datetime
import json
from django.conf import settings
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.formtools.wizard.views import SessionWizardView

from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext
import mercadopago
from lacalma.models import Reserva, Departamento
from lacalma.forms import ReservaForm1, ReservaForm2




class ReservaWizard(SessionWizardView):
    _reserva = None

    def get_template_names(self):
        return 'step_%s.html' % self.steps.current

    def get_context_data(self, form, **kwargs):

        context = super(ReservaWizard, self).get_context_data(form=form, **kwargs)
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
        context['deptos'] = Departamento.objects.all()

        if self.steps.current != 'fechas':
            fe = self.get_form('fechas', data=self.storage.get_step_data('fechas'))
            fe.is_valid()
            reserva = Reserva(desde=fe.cleaned_data['desde'],
                              hasta=fe.cleaned_data['hasta'],
                              departamento=fe.cleaned_data['departamento'])
            reserva.calcular_costo()
            reserva.calcular_vencimiento()
            context['reserva'] = reserva
        return context

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        del data['fechas']
        reserva = Reserva(**data)
        reserva.calcular_vencimiento()
        reserva.save()

        if reserva.forma_pago == 'deposito':

            mail_txt = render_to_string('mail_txt.html', {'reserva': reserva})
            mail_html = render_to_string('mail.html', {'reserva': reserva})

            msg = EmailMultiAlternatives('Reserva en La Calma - Las Grutas /ref. #%s' % reserva.id,
                                   mail_txt, 'info@lacalma-lasgrutas.com.ar', [reserva.email],
                                   bcc=['info@lacalma-lasgrutas.com.ar'])
            msg.attach_alternative(mail_html, "text/html")
            msg.send()

            return redirect('/gracias/')
        else:
            mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)

            title = "La Calma {}: {} al {} inclusive".format(reserva.departamento.nombre,
                                                             reserva.desde.strftime("%d/%m/%Y"),
                                                             (reserva.hasta - timedelta(days=1)).strftime("%d/%m/%Y"))

            preference = {
                "items": [
                    {
                        "id": str(reserva.id),
                        "title": title,
                        "quantity": 1,
                        "currency_id": "ARS",
                        "unit_price": float(reserva.costo_total)
                    }
                ],
                "payer": {
                    "name": reserva.nombre_y_apellido,
                    "email": reserva.email,
                    "date_created": reserva.created.isoformat(),
                },
                "back_urls": {
                    "success": "http://reserva.lacalma-lasgrutas.com.ar/gracias",
                },
                "auto_return": "approved",
            }



            preference = mp.create_preference(preference)
            import ipdb; ipdb.set_trace()
            url = preference['response']['sandbox_init_point'];

            return redirect(url)


def gracias(request):
    return render(request, 'gracias.html', {'gracias': True})


@staff_member_required
def detalle(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    return render(request, 'index.html', {'reserva': reserva, 'presupuesto': True})


@csrf_exempt
def mp_notification(request):
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    mp.sandbox_mode(True)
    payment_info = mp.get_payment_info(request.GET["id"])
    import ipdb; ipdb.set_trace()



reserva_view = ReservaWizard.as_view([('fechas', ReservaForm1), ('datos', ReservaForm2)])


"""
A futuro. la inmobiliaria manejaba su propio calendario de ubicacion.

http://sanmatiaspropiedades.com/api-v2/rentals/www_query_all

76251878  La Calma 1
76251879  La Calma 2
76251910  La Calma 3
76251909  La Calma 4
"""