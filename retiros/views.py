# -*- coding: utf-8 -*-
import json
import uuid

from django.shortcuts import render, get_object_or_404, redirect
from .forms import InscripcionForm
from .models import Retiro, Inscripcion
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings


import mercadopago


def inscripcion(request, retiro_id):

    retiro = get_object_or_404(Retiro, id=retiro_id)
    data = request.POST if request.method == 'POST' else None
    instance = Inscripcion.objects.first() if not data else None
    form = InscripcionForm(data, instance=instance)
    if form.is_valid():
        inscripcion = form.save(commit = False)
        inscripcion.retiro = retiro

        inscripcion.save()

        if inscripcion.forma_pago == 'deposito':

            mail_txt = render_to_string('retiros/mail_txt.html', {'inscripcion': inscripcion})
            for to in (inscripcion.email, settings.EMAIL_ADMIN_RETIROS):
                send_mail(u'Pre-Inscripción - Centro Sivananda /ref #%s' % inscripcion.id,
                          mail_txt, settings.EMAIL_ADMIN_RETIROS, [to])
            return redirect('retiros_gracias')
        else:

            inscripcion.mp_id = str(uuid.uuid1())
            site = Site.objects.get_current()


            mp = mercadopago.MP(settings.MP_SIVANANDA_CLIENT_ID, settings.MP_SIVANANDA_CLIENT_SECRET)

            title = "{} - Inscripcion".format(inscripcion.retiro)
            preference = {
                "items": [
                    {
                        "id": str(inscripcion.id),
                        "title": title,
                        "quantity": 1,
                        "currency_id": "ARS",
                        "unit_price": float(inscripcion.costo_total)
                    }
                ],
                "payer": {
                    "name": inscripcion.nombre_completo,
                    "email": inscripcion.email,
                },
                "back_urls": {
                    "success": site.domain + reverse('retiros_gracias_mp'),
                },
                "auto_return": "approved",
                "external_reference": inscripcion.mp_id,
                "notification_url": site.domain + reverse('retiros_ipn'),
            }

            preference = mp.create_preference(preference)

            if settings.MP_SANDBOX_MODE:
                url = preference['response']['sandbox_init_point']
            else:
                url = preference['response']['init_point']
            inscripcion.mp_url = url
            inscripcion.save(update_fields=['mp_id', 'mp_url'])
            return redirect(url)

    return render(request, 'retiros/inscripcion.html', {'form': form, 'retiro': retiro})



def gracias(request):
    return render(request, 'retiros/gracias.html')


def gracias_mp(request):
    return render(request, 'retiros/gracias_mp.html')

def normas(request):
    return render(request, 'retiros/normas.html')


@csrf_exempt
def mp_notification(request):
    mp = mercadopago.MP(settings.MP_SIVANANDA_CLIENT_ID, settings.MP_SIVANANDA_CLIENT_SECRET)
    if settings.MP_SANDBOX_MODE:
        mp.sandbox_mode(True)


    if request.GET.get('topic', '') == 'payment':
        site = Site.objects.get_current()

        payment_info = mp.get_payment_info(request.GET["id"])
        print(payment_info)
        if payment_info['status'] == 200:
            mp_id = payment_info['response']['collection']['external_reference']
            status = payment_info['response']['collection']['status']
            if status == 'approved':
                inscripcion = get_object_or_404(Inscripcion, mp_id=mp_id)

                inscripcion.estado = inscripcion.ESTADOS.confirmada
                inscripcion.fecha_deposito_reserva = timezone.now()
                inscripcion.deposito_reveserva = inscripcion.costo_total
                inscripcion.save()



                mail_txt = render_to_string('retiros/mail_mp_txt.html', {'inscripcion': inscripcion})
                for to in (inscripcion.email, settings.EMAIL_ADMIN_RETIROS, 'gracielamothe@gmail.com'):

                    send_mail(u'Inscripción Confirmada - Centro Sivananda /ref #%s' % inscripcion.id,
                      mail_txt, settings.EMAIL_ADMIN_RETIROS, [to])

            return HttpResponse('ok')
    return HttpResponseBadRequest('bad boy')


