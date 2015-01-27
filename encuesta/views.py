from django.shortcuts import render, redirect, get_object_or_404
from .forms import EncuestaForm
from .models import EncuestaSatisfaccion
from lacalma.models import Reserva
from django.template.loader import render_to_string
from django.core.mail import send_mail



# Create your views here.


def gracias(request):
    return render(request, 'encuesta_gracias.html')

def completa(request):
    return render(request, 'completa.html')


def encuesta(request, uuid):
    reserva = get_object_or_404(Reserva, uuid=uuid)
    try:
        reserva.encuesta.get()
        return redirect('encuesta_completa')
    except EncuestaSatisfaccion.DoesNotExist:
        pass

    data = request.POST if request.method == 'POST' else None
    form = EncuestaForm(data)
    if form.is_valid():
        encuesta = form.save(commit=False)
        encuesta.reserva_relacionada = reserva
        encuesta.save()

        mail_txt = render_to_string('mail_admin_encuesta.completa.html', {'encuesta': encuesta})
        send_mail('[La Calma] Nueva encuesta ref #%s' % encuesta.reserva_relacionada.id, mail_txt,
                'info@lacalma-lasgrutas.com.ar', ['info@lacalma-lasgrutas.com.ar'])

        return redirect('encuesta_gracias')
    return render(request, 'encuesta.html', {'form': form, 'reserva': reserva})