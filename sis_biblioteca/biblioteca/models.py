# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PessoaFisica(models.Model):
    nome = models.CharField('Nome', max_length=120)
    username = models.CharField('Nome de Usuário', max_length=120)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'


class Biblioteca(models.Model):
    nome = models.CharField('Nome', max_length=120)
    uo = models.CharField('Campus', max_length=120)

    def __unicode__(self):
        return '{} - {}'.format(self.nome, self.uo)

    class Meta:
        verbose_name = 'Biblioteca'
        verbose_name_plural = 'Bibliotecas'


class Titulo(models.Model):
    nome = models.CharField('Nome', max_length=120)
    categoria = models.CharField('Categoria', max_length=60)
    imagem = models.ImageField('Imagem')

    def __unicode__(self):
        return '{} ({})'.format(self.nome, self.categoria)

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'


class Exemplar(models.Model):
    biblioteca = models.ForeignKey('biblioteca.Biblioteca', verbose_name='Biblioteca')
    titulo = models.ForeignKey('biblioteca.Titulo', verbose_name='Título')
    data_aquisicao = models.DateField('Data de Aquisição')

    def __unicode__(self):
        return '{} ({})'.format(self.titulo.nome, self.biblioteca.nome)

    class Meta:
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'


class Emprestimo(models.Model):
    exemplar = models.ForeignKey('biblioteca.Exemplar')
    data = models.DateField('Data', auto_now_add=True)
    usuario = models.ForeignKey('auth.User', verbose_name='Usuário')
    data_prevista_devolucao = models.DateField('Data Prevista para a Devolução')
    data_devolucao = models.DateField('Data', null=True, blank=True)

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'