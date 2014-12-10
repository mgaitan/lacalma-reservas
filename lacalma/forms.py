# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import forms
from lacalma.models import Reserva, Departamento


class ReservaAdminForm(forms.ModelForm):
    class Meta:
        model = Reserva

    def clean(self):
        cleaned_data = super(ReservaAdminForm, self).clean()
        if not Reserva.fecha_libre(cleaned_data['departamento'], cleaned_data['desde'], cleaned_data['hasta'], exclude=self.instance):
            raise forms.ValidationError('Hay reservas realizadas durante estas fechas para este departamento')

        return cleaned_data



class ReservaForm1(forms.Form):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label=None)
    desde = forms.DateField(required=False, widget=forms.HiddenInput)
    hasta = forms.DateField(required=False, widget=forms.HiddenInput, )
    fechas = forms.CharField(label='¿Durante qué días quiere reservar?',
                help_text='Seleccione hasta la última noche que duerme', required=False)

    def __init__(self, *args, **kwargs):
        super(ReservaForm1, self).__init__(*args, **kwargs)
        self.fields['departamento'].widget = forms.HiddenInput()
        self.fields['departamento'].initial = Departamento.objects.all()[0]
        self.fields['fechas'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ReservaForm1, self).clean()

        if not cleaned_data.get('desde', False) or not cleaned_data.get('hasta', False):
            try:
                desde, hasta = [datetime.strptime(d, "%d/%m/%Y").date() for d in cleaned_data.get("fechas").split(' al ')]
                hasta += timedelta(days=1)
            except:
                raise forms.ValidationError(u"Rango de fecha no válido")

            cleaned_data['desde'] = desde
            cleaned_data['hasta'] = hasta

        if not Reserva.fecha_libre(cleaned_data['departamento'],
                                   cleaned_data['desde'],
                                   cleaned_data['hasta']):
            self.add_error('fechas', 'Hay reservas realizadas durante esas fechas para este departamento')

        return cleaned_data


class ReservaForm2(forms.ModelForm):
    CHOICES = (('deposito', u'Realizaré una seña del 50% vía transferencia bancaria en las próximas 48hs'),
               ('mercadopago', 'Abonaré con tarjeta de crédito (hasta 12 cuotas)'))
    forma_pago = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial='deposito')

    def __init__(self, *args, **kwargs):
        super(ReservaForm2, self).__init__(*args, **kwargs)
        for field in ('nombre_y_apellido', 'email', 'telefono'):
            self.fields[field].required = True

    class Meta:
        model = Reserva
        fields = ('nombre_y_apellido', 'email', 'telefono', 'procedencia',
                  'como_se_entero', 'comentario', 'forma_pago')

