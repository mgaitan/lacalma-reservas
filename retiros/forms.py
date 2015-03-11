# -*- coding: utf-8 -*-
from django import forms
from .models import Inscripcion


class InscripcionForm(forms.ModelForm):
    CHOICES = (('deposito', u'Realizaré una seña del 50% vía transferencia bancaria en las próximas 48hs'),
               ('mercadopago', 'Abonaré con tarjeta de crédito (hasta 12 cuotas)'))


    acepto = forms.BooleanField(u'He leído y acepto las Normas de Funcionamiento')

    forma_pago = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial='deposito')
    email_confirma = forms.EmailField(label='Confirme su email')


    class Meta:
        model = Inscripcion
        fields = ['apellido', 'nombres', 'fecha_nacimiento', 'documento',
                  'ciudad', 'provincia', 'pais', 'telefono', 'email', 'email_confirma',
                  'estado_civil', 'enfermedades', 'medicamentos',
                  'contacto_emergencia', 'telefono_emergencia', 'practica_desde',
                  'lugar_practica', 'medio_noticia', 'comentario', 'acepto', 'forma_pago']


    def clean(self):
        cleaned_data = super(InscripcionForm, self).clean()
        if cleaned_data['email'] != cleaned_data.get('email_confirma'):
            self.add_error('email', 'Las direcciones no coinciden')
        return cleaned_data
