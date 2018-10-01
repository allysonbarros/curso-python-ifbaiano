# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from biblioteca.forms import LoginForm, PessoaFisicaForm
from biblioteca.models import Emprestimo, Exemplar


@login_required(login_url='/login/')
def index(request):
    title = 'Dashboard'

    eh_admistrador = request.user.groups.filter(name='Administrador').exists()
    eh_bibliotecario = request.user.groups.filter(name='Bibliotecario').exists()
    eh_atendente = request.user.groups.filter(name='Atendente').exists()
    eh_usuario = request.user.groups.filter(name='Usuario').exists()

    if eh_usuario:
        ultimos_emprestimos = Emprestimo.objects.filter(usuario__username=request.user.username)[:5]
        emprestimos_a_vencer = Emprestimo.vencem_na_proxima_semana.filter(usuario__username=request.user.username).order_by('data_prevista_devolucao')[:5]

    if eh_bibliotecario:
        ultimos_exemplares = Exemplar.objects.all().order_by('data_aquisicao')[:10]
    return render(request, 'index.html', locals())

def form_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        user = form.realizar_autenticacao()
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/')

    return render(request, 'login.html', locals())

def logoff(request):
    logout(request)
    return redirect('/')

# def autenticar(request):
#     if request.method == 'GET':
#         raise ValidationError('O método não pode ser GET')

#     usuario = request.POST.get('usuario')
#     senha = request.POST.get('senha')

#     user = authenticate(username=usuario, password=senha)
#     if user is None:
#         raise ValidationError('Usuário não encontrado.')
#     else:
#         login(request, user)
#         return redirect('/')

@login_required(login_url='/login/')
def emprestimos(request):
    if request.user.is_authenticated() and not request.user.groups.filter(name='Usuario'):
        return HttpResponseForbidden('Acesso Negado')

    title = 'Meus Empréstimos'
    emprestimos = Emprestimo.objects.filter(usuario__username=request.user.username)

    return render(request, 'emprestimos.html', locals())

@login_required(login_url='/login/')
def renovar_emprestimo(request, id):
    title = 'Renovação de Empréstimo'

    # try:
    #     obj = Emprestimo.objects.get(pk=id)
    # except Emprestimo.DoesNotExist:
    #     return HttpResponse('Emprestimo não encontrado.', status=404)

    obj = get_object_or_404(Emprestimo.vencem_na_proxima_semana, pk=id)
    if obj.usuario.username != request.user.username:
        return HttpResponse('Acesso Negado.', status=403)

    obj.data_prevista_devolucao = datetime.datetime.today() + timedelta(days=7)
    obj.save()

    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    send_mail(
        'SisBiblioteca - Renovação de Empréstimo',
        '''
        Olá {nome}, sua renovação foi realizada com sucesso!

        A data para a devolução do exemplar é {data}.
        '''.format(
            nome=obj.usuario,
            data=obj.data_prevista_devolucao.strftime("%d/%m/%Y")
        ),
        'sisbiblioteca@ifbaiano.edu.br',
        ['a@a.com'],
        fail_silently=True
    )

    # EmailMessage(
    #     'SisBiblioteca - Renovação de Empréstimo',
    #     '''
    #     Olá {nome}, sua renovação foi realizada com sucesso!
    #
    #     A data para a devolução do exemplar é {data}.
    #     '''.format(nome=obj.usuario,data=obj.data_prevista_devolucao.strftime("%d/%m/%Y")),
    #     'sisbiblioteca@ifbaiano.edu.br',
    #     ['a@a.com'],
    #     ['gti@ifbaiano.edu.br'],
    #     reply_to=['bibliotecas@ifbaiano.edu.br'],
    # ).send(fail_silently=True)

    messages.success(request, 'O empréstimo foi renovado com sucesso.')
    return redirect('/biblioteca/emprestimos/')

@login_required(login_url='/login/')
@permission_required('biblioteca.add_pessoafisica', login_url='/login/', raise_exception=True)
def cadastrar_pessoa_fisica(request):
    form = PessoaFisicaForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'cadastrar_pessoa_fisica.html', locals())




# def somar2(request):
#     try:
#         a = int(request.GET.get('a', 0))
#         b = int(request.GET.get('b', 0))
#         resultado = a + b
#     except ValueError:
#         raise Exception('Informe dois valores inteiros.')
#
#     return render(request, 'calculadora.html', locals())
#
#
# def somar(request, a, b):
#     print dir(request)
#     resultado = int(a) + int(b)
#     return render(request, 'calculadora.html', locals())
#
#
# def hello_world(request):
#     emprestimos = Emprestimo.ativos.all()
#     return render(request, 'hello_world.html', locals())
