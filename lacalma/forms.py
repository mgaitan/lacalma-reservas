# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from lacalma.models import Reserva, Departamento



class ReservaForm(forms.ModelForm):
    desde = forms.CharField(widget=forms.HiddenInput, required=False)
    hasta = forms.CharField(widget=forms.HiddenInput, required=False)
    fechas = forms.CharField(label='¿Durante qué días quiere reservar?',
                help_text='Seleccione hasta la última noche que duerme')

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['departamento'].widget = forms.HiddenInput()
        self.fields['departamento'].initial = Departamento.objects.all()[0]
        self.fields['fechas'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ReservaForm, self).clean()
        try:
            desde, hasta = [datetime.strptime(d, "%d-%m-%Y").date() for d in cleaned_data.get("fechas").split(' al ')]
            hasta += timedelta(days=1)
        except:
            raise forms.ValidationError(u"Rango de fecha no válido")

        if not Reserva.fecha_libre(cleaned_data['departamento'], desde, hasta):
            self.add_error('fechas', 'Hay reservas realizadas durante esas fechas para este departamento')

        return cleaned_data

    class Meta:
        model = Reserva
        fields = ('departamento', 'fechas', 'desde', 'hasta', 'nombre_y_apellido', 'email',
                  'procedencia', 'telefono', 'como_se_entero', 'comentario')

