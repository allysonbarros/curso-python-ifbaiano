# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from biblioteca import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^emprestimos?[/]$', views.emprestimos, name='emprestimos'),
    url(r'^cadastrar_pessoa_fisica/$', views.cadastrar_pessoa_fisica, name='cadastrar_pessoa_fisica'),
    url(r'^renovar_emprestimo/(?P<id>\d+)/$', views.renovar_emprestimo, name='renovar_emprestimo'),

    # url(r'^hello_world?[/]$', views.hello_world, name='hello_world'),
    # url(r'^somar_2/$', views.somar2, name='somar2'),
    # url(r'^somar/(?P<a>\d)/(?P<b>\d)/$', views.somar, name='somar'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
