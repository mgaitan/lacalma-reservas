# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from lacalma.models import Reserva


class ReservaForm(forms.ModelForm):
    desde = forms.CharField(widget=forms.HiddenInput, required=False)
    hasta = forms.CharField(widget=forms.HiddenInput, required=False)
    fechas = forms.CharField(label='Que fecha quiere reservar?')

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['departamento'].widget.choices = [c for c in self.fields['departamento'].widget.choices][1:]


    def clean(self):
        cleaned_data = super(ReservaForm, self).clean()
        try:
            desde, hasta = [datetime.strptime(d, "%d-%m-%Y").date() for d in cleaned_data.get("fechas").split(' al ')]
        except:
            msg = u"Rango de fecha no válido"
            self.add_error('fechas', msg)

        cleaned_data['desde'] = desde
        cleaned_data['hasta'] = hasta + timedelta(days=1)   # dia de salida
        return cleaned_data



    class Meta:
        model = Reserva
        fields = ('departamento', 'fechas', 'desde', 'hasta', 'nombre_y_apellido', 'email',
                  'procedencia', 'telefono', 'whatsapp', 'como_se_entero')

