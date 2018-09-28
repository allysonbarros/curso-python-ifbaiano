# -*- coding: utf-8 -*-
"""sis_biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from biblioteca import views as bib_views

urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^$', bib_views.index, name='index'),
    url(r'^biblioteca/', include('biblioteca.urls')),
    url(r'^admin/', admin.site.urls),

    # Autenticação
    url(r'^login/$', bib_views.form_login, name='login'),
    # url(r'^autenticar/$', bib_views.autenticar, name='autenticar'),
    url(r'^logoff/$', bib_views.logoff, name='logoff'),
]
