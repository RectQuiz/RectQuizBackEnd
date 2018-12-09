from django import forms
from django.contrib.auth.models import User
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Seu Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Seu Sobrenome'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Seu apelido no sistema'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Seu Email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Sua senha'})
        }

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'descricao', 'fundo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome do tema'}),
            'descricao': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descreva rapidamente'}),
            'fundo': forms.FileInput(attrs={'class':'form-control', 'required':'false'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("fundo", None)
        if file:
            if file.content_type.split('/')[0] not in ['image']:
                raise forms.ValidationError('Enviar apenas imagem.')
            if file.content_type == 'image/bmp':
                raise forms.ValidationError('Arquivos .BMP não permitidos.')
        return cleaned_data

class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['titulo', 'descricao', 'tema']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome do Nível'}),
            'descricao': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descreva rapidamente'}),
            'tema': forms.TextInput(attrs={'class':'form-control', 'type': 'hidden'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['pergunta', 'a', 'b', 'c', 'd', 'resposta', 'nivel']
        widgets = {
            'pergunta': forms.Textarea(attrs={'class':'form-control', 'rows':'5', 'placeholder':'Descreva rapidamente'}),
            'a': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Alternativa A'}),
            'b': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Alternativa B'}),
            'c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa C'}),
            'd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa D'}),
            'resposta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resposta'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}),
        }