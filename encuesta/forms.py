# -*- coding: utf-8 -*-
from django import forms
from encuesta.models import EncuestaSatisfaccion


class EncuestaForm(forms.ModelForm):

    class Meta:
        model = EncuestaSatisfaccion

