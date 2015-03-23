# -*- coding: utf-8 -*-
from django import forms
from .models import Inscripcion
from descuentos.models import CodigoDeDescuento


class InscripcionForm(forms.ModelForm):
    # CHOICES = (('mercadopago', 'Abonaré con tarjeta de crédito (hasta 12 cuotas)'),)


    acepto = forms.BooleanField(u'He leído y acepto las Normas de Funcionamiento')

    forma_pago = forms.CharField(widget=forms.HiddenInput, initial='mercadopago')
    email_confirma = forms.EmailField(label='Confirme su email')
    codigo_descuento = forms.CharField(label=u'¿Tiene un código de descuento?', required=False)


    class Meta:
        model = Inscripcion
        fields = ['apellido', 'nombres', 'fecha_nacimiento', 'documento',
                  'ciudad', 'provincia', 'pais', 'telefono', 'email', 'email_confirma',
                  'estado_civil', 'enfermedades', 'medicamentos',
                  'contacto_emergencia', 'telefono_emergencia', 'practica_desde',
                  'lugar_practica', 'medio_noticia', 'comentario', 'acepto', 'codigo_descuento', 'forma_pago']


    def clean_codigo_descuento(self):
        data = self.cleaned_data.get('codigo_descuento', None)
        if data:
            try:
                codigo = CodigoDeDescuento.objects.get(codigo=data)
                return codigo
            except CodigoDeDescuento.DoesNotExist:
                return None
        return None


    def clean(self):
        cleaned_data = super(InscripcionForm, self).clean()
        if cleaned_data['email'] != cleaned_data.get('email_confirma'):
            self.add_error('email', 'Las direcciones no coinciden')
        return cleaned_data
