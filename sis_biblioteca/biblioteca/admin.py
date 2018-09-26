# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from biblioteca.models import Biblioteca, Exemplar, Titulo, PessoaFisica, Emprestimo


class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'username')
    search_fields = ('nome', 'username')
admin.site.register(PessoaFisica, PessoaFisicaAdmin)


class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uo')
    search_fields = ('nome',)
admin.site.register(Biblioteca, BibliotecaAdmin)


class TituloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'imagem')
    list_filter = ('categoria',)
    search_fields = ('nome',)
admin.site.register(Titulo, TituloAdmin)


class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_aquisicao', 'biblioteca')
    list_filter = ('biblioteca',)
    date_hierarchy = 'data_aquisicao'
    search_fields = ('titulo',)
admin.site.register(Exemplar, ExemplarAdmin)


class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('exemplar', 'data', 'usuario', 'data_prevista_devolucao', 'data_devolucao')
    list_filter = ('exemplar', 'usuario')
    date_hierarchy = 'data'
    search_fields = ('exemplar__titulo__nome',)
admin.site.register(Emprestimo, EmprestimoAdmin)