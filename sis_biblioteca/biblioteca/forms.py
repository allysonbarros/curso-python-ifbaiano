# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

from django import forms
from django.contrib.auth import authenticate

from biblioteca.models import Campus, Titulo, Categoria, PessoaFisica, Emprestimo, Exemplar


class CampusForm(forms.ModelForm):
    def clean_nome(self):
        nome_digitado = self.cleaned_data.get('nome')
        if Campus.objects.exclude(pk=self.instance.pk).filter(
                nome__iexact=nome_digitado
        ).exists():
            raise forms.ValidationError('O Campus informado já está cadastrado no sistema.')
        return self.cleaned_data.get('nome')

    class Meta:
        model = Campus
        fields = ('nome',)

class PessoaFisicaForm(forms.ModelForm):
    # sexo = forms.ChoiceField(
    #     choices=PessoaFisica.SEXO_CHOICES,
    #     widget=forms.RadioSelect()
    # )

    def clean_username(self):
        username_digitado = self.cleaned_data.get('username')
        if PessoaFisica.objects.exclude(pk=self.instance.pk).filter(
                username__iexact=username_digitado
        ).exists():
            raise forms.ValidationError('O username informado já está em uso.')
        return self.cleaned_data.get('username')

    class Meta:
        model = PessoaFisica
        fields = ('__all__')

class TituloForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        help_text='Selecione uma ou mais categorias.',
        widget=forms.CheckboxSelectMultiple()
    )

    def clean_categorias(self):
        categorias_selecionadas = self.cleaned_data.get('categorias')
        if len(categorias_selecionadas) != 0 and len(categorias_selecionadas) != 3:
            raise forms.ValidationError('Por favor, selecione 3 categorais.')

        return self.cleaned_data.get('categorias')

    class Meta:
        model = Titulo
        fields = ('nome', 'categorias', 'imagem', 'capitulo_exemplo')

class EmprestimoForm(forms.ModelForm):
    exemplar = forms.ModelChoiceField(queryset=Exemplar.objects.all())

    def clean_usuario(self):
        usuario_selecionado = self.cleaned_data.get('usuario')
        if Emprestimo.objects.filter(
                usuario=usuario_selecionado,
                data_devolucao__isnull=True
        ).exists():
            raise forms.ValidationError('O usuário selecionado não pode realizar um novo empréstimo')

        return self.cleaned_data.get('usuario')

    def __init__(self, *args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)
        emprestimos = Emprestimo.objects.filter(data_devolucao__isnull=True)
        self.fields['exemplar'].queryset = Exemplar.objects.exclude(emprestimo__in=emprestimos)
        self.fields['usuario'].queryset = PessoaFisica.objects.exclude(emprestimo__in=emprestimos)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.data_prevista_devolucao = datetime.datetime.today() + timedelta(days=7)

        return super(EmprestimoForm, self).save(commit)

    class Meta:
        model = Emprestimo
        fields = ('exemplar', 'usuario')


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, label='Login')
    senha = forms.CharField(max_length=50, label='Senha', widget=forms.PasswordInput())

    def clean_login(self):
        login_digitado = self.cleaned_data.get('login')
        if len(login_digitado) <= 4:
            raise forms.ValidationError('O login digitado deve ser maior que 4 caracteres')
        return self.cleaned_data.get('login')

    def realizar_autenticacao(self):
        login = self.cleaned_data.get('login')
        senha = self.cleaned_data.get('senha')
        return authenticate(username=login, password=senha)