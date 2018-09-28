# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from biblioteca.forms import TituloForm, PessoaFisicaForm, CampusForm, EmprestimoForm
from biblioteca.models import Biblioteca, Campus, Categoria, PessoaFisica, Titulo, Exemplar, Emprestimo

admin.site.index_title = 'IFBaiano - Curso de Python e Django'
admin.site.site_header = 'Minha do Cópia do SUAP'

class BiblitecaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'campus')
    list_filter = ('campus',)
admin.site.register(Biblioteca, BiblitecaAdmin)

class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    form = CampusForm
admin.site.register(Campus, CampusAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
admin.site.register(Categoria, CategoriaAdmin)

class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'username', 'sexo')
    form = PessoaFisicaForm
admin.site.register(PessoaFisica, PessoaFisicaAdmin)

class TituloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'meu_metodo', 'minha_imagem', 'minha_imagem2', 'download_capitulo_exemplo')
    form = TituloForm
    # fieldsets = (
    #     ('Digite o Nome do Exemplar', {
    #         'fields': ('nome',)
    #     }),
    #     ('Selecione as Categorias deste Exemplar', {
    #         'fields': ('categorias',)
    #     }),
    #     ('Faça o upload dos arquivos abaixo', {
    #         'classes': ('wide',),
    #         'fields': ('imagem', 'capitulo_exemplo'),
    #     }),
    # )

    def meu_metodo(self, obj):
        categorias = []
        for categoria in obj.categorias.all():
            categorias.append(categoria.nome)
        return ', '.join(categorias)
    meu_metodo.short_description = 'Categorias'

    def minha_imagem(self, obj):
        return '<img style="height: 180px;" src="/static/{}" />'.format(obj.imagem)
    minha_imagem.allow_tags = True

    def minha_imagem2(self, obj):
        return '<a href="/{url}">{url}</a>'.format(url=obj.imagem)
    minha_imagem2.allow_tags = True

    def download_capitulo_exemplo(self, obj):
        if obj.capitulo_exemplo:
            return '<a class="button" href="/{url}">Visualizar PDF</a>'.format(url=obj.capitulo_exemplo)
        else:
            return '<a class="button" disabled="disabled">Visualizar PDF</a>'
    download_capitulo_exemplo.allow_tags = True

admin.site.register(Titulo, TituloAdmin)

class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'biblioteca', 'data_aquisicao')
    list_filter = ('biblioteca',)
    search_fields = ('titulo__nome', 'biblioteca__nome', 'biblioteca__campus__nome')
    date_hierarchy = 'data_aquisicao'
admin.site.register(Exemplar, ExemplarAdmin)

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('exemplar', 'usuario', 'data_emprestimo', 'data_prevista_devolucao', 'data_devolucao')
    form = EmprestimoForm

    def get_queryset(self, request):
        if request.user.groups.filter(name='Usuario').exists():
            return Emprestimo.objects.filter(usuario__username=request.user.username)

        # if not request.user.is_superuser:
        #     return Emprestimo.objects.filter(usuario__username=request.user.username)

        return super(EmprestimoAdmin, self).get_queryset(request)


admin.site.register(Emprestimo, EmprestimoAdmin)
