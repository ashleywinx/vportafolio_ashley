# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from appportafolio.models import *
from django import forms
from .models import Tarea

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'imagen'] # Especifica los campos que deseas incluir
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenido'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})#,
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['tarea', 'fecha_tarea', 'fkestado']
        widgets = {
            'tarea': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder': 'Escribe tu tarea aquí'}),
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fkestado': forms.Select(attrs={'class': 'form-control'}),
        }
