# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from django.db.models import Q
from lacalma.models import Reserva



class ReservaForm(forms.ModelForm):
    desde = forms.CharField(widget=forms.HiddenInput, required=False)
    hasta = forms.CharField(widget=forms.HiddenInput, required=False)
    fechas = forms.CharField(label='¿Durante qué días quiere reservar?',
                help_text='Seleccione hasta la última noche que duerme')

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['departamento'].empty_label = None


    def clean(self):
        cleaned_data = super(ReservaForm, self).clean()
        try:
            desde, hasta = [datetime.strptime(d, "%d-%m-%Y").date() for d in cleaned_data.get("fechas").split(' al ')]
            hasta += timedelta(days=1)
        except:
            msg = u"Rango de fecha no válido"
            self.add_error('fechas', msg)

        cleaned_data['desde'] = desde
        cleaned_data['hasta'] = hasta  # + timedelta(days=1)   # dia de salida

        # ( start1 <= end1 and start2 <= end2 )
        # import ipdb; ipdb.set_trace()
        if Reserva.objects.filter(departamento=cleaned_data['departamento']).\
                           exclude(estado=Reserva.ESTADOS.vencida).filter(
                                  Q(desde__range=(desde, hasta - timedelta(days=1))) |
                                  Q(hasta__range=(desde + timedelta(days=1), hasta)) |
                                  Q(desde__lte=desde,hasta__gte=hasta)).exists():

            self.add_error('fechas', 'Hay reservas realizadas durante esas fechas')

        return cleaned_data



    class Meta:
        model = Reserva
        fields = ('departamento', 'fechas', 'desde', 'hasta', 'nombre_y_apellido', 'email',
                  'procedencia', 'telefono', 'como_se_entero', 'comentario')

