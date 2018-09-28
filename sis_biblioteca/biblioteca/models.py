# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models


class PessoaFisica(models.Model):
    MASCULINO_CHOICE = 'M'
    FEMININO_CHOICE = 'F'

    SEXO_CHOICES = (
        (MASCULINO_CHOICE, 'Masculino'),
        (FEMININO_CHOICE, 'Feminino')
    )

    nome = models.CharField('Nome', max_length=60)
    username = models.CharField('Nome de Usuário', max_length=120)
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES, null=True)

    def __unicode__(self):
        return '{} ({})'.format(self.nome, self.username)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'


class Campus(models.Model):
    nome = models.CharField('Nome', max_length=120, unique=True)

    # def clean(self):
    #     if Campus.objects.exclude(pk=self.pk).filter(nome__icontains=self.nome):
    #         raise ValidationError('Já existe um campus com o nome inserido.')
    #
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.clean()
    #     super(Campus, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'


class Biblioteca(models.Model):
    nome = models.CharField('Nome', max_length=120)
    campus = models.ForeignKey('biblioteca.Campus', verbose_name='Campus')

    def __unicode__(self):
        return '{} - {}'.format(self.nome, self.campus)

    class Meta:
        verbose_name = 'Biblioteca'
        verbose_name_plural = 'Bibliotecas'


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=60)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Titulo(models.Model):
    nome = models.CharField('Nome', max_length=120)
    categorias = models.ManyToManyField('biblioteca.Categoria', verbose_name='Categorias')
    imagem = models.ImageField('Imagem', upload_to='static/uploads/imagens/')
    capitulo_exemplo = models.FileField('Capítulo de Exemplo', upload_to='static/uploads/pdfs/', null=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'


class Exemplar(models.Model):
    biblioteca = models.ForeignKey('biblioteca.Biblioteca', verbose_name='Biblioteca')
    titulo = models.ForeignKey('biblioteca.Titulo', verbose_name='Título')
    data_aquisicao = models.DateField('Data da Aquisição')

    def __unicode__(self):
        return '{} #{} - {}'.format(self.titulo.nome, self.pk, self.biblioteca.nome)

    class Meta:
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'

class EmprestimosAtivosManager(models.Manager):
    def get_queryset(self):
        return super(EmprestimosAtivosManager, self).get_queryset().filter(data_devolucao__isnull=True)

class EmprestimosFinalizadosManager(models.Manager):
    def get_queryset(self):
        return super(EmprestimosFinalizadosManager, self).get_queryset().exclude(data_devolucao__isnull=True)

class EmprestimosProximosVencimentoManager(models.Manager):
    def get_queryset(self):
        data_hoje = datetime.today()
        proxima_semana = data_hoje + timedelta(days=7)
        return super(EmprestimosProximosVencimentoManager, self).get_queryset().filter(
            data_prevista_devolucao__gte=data_hoje,
            data_prevista_devolucao__lt=proxima_semana,
        )


class Emprestimo(models.Model):
    exemplar = models.ForeignKey('biblioteca.Exemplar', verbose_name='Exemplar')
    usuario = models.ForeignKey('biblioteca.PessoaFisica', verbose_name='Usuário')
    data_emprestimo = models.DateField('Data do Empréstimo', auto_now_add=True)
    data_prevista_devolucao = models.DateField('Data Prevista para Devolução', null=True, blank=True)
    data_devolucao = models.DateField('Data da Devolução', null=True, blank=True)

    objects = models.Manager()
    ativos = EmprestimosAtivosManager()
    finalizados = EmprestimosFinalizadosManager()
    vencem_na_proxima_semana = EmprestimosProximosVencimentoManager()

    def is_ativo(self):
        return self.data_devolucao is None

    def em_atraso(self):
        return self.data_prevista_devolucao >= datetime.today()

    def __unicode__(self):
        return 'Empréstimo do "{}" para "{}"'.format(self.exemplar.titulo.nome, self.usuario.nome)

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
