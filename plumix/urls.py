"""
URL configuration for plumix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plumixapp.views import *
from django.urls import path, re_path, include
from django.urls import path
from  django.contrib.auth import views as auth_views
from django.urls import path
from plumixapp import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/export/', views.dashboard_export_csv, name='dashboard_export_csv'),
    path("", index, name="index"),
    #path("login/", login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('usuarioapp.urls')),
# Granja
    path('granjas/', login_required(views.granja_list), name='granja_list'),
    path('granjas/novo/', login_required(views.granja_create), name='granja_create'),
    path('granjas/<int:pk>/editar/', login_required(views.granja_update), name='granja_update'),
    path('granjas/<int:pk>/excluir/', login_required(views.granja_delete), name='granja_delete'),

    # Galpão
    path('galpoes/', login_required(views.galpao_list), name='galpao_list'),
    path('galpoes/novo/', login_required(views.galpao_create), name='galpao_create'),
    path('galpoes/<int:pk>/editar/', login_required(views.galpao_update), name='galpao_update'),
    path('galpoes/<int:pk>/excluir/', login_required(views.galpao_delete), name='galpao_delete'),

    # Lote
    path('lotes/', login_required(views.lote_list), name='lote_list'),
    path('lotes/novo/', login_required(views.lote_create), name='lote_create'),
    path('lotes/<int:pk>/editar/', login_required(views.lote_update), name='lote_update'),
    path('lotes/<int:pk>/excluir/', login_required(views.lote_delete), name='lote_delete'),

    # Ambiente
    path('ambiente/', login_required(views.ambiente_list), name='ambiente_list'),
    path('ambiente/novo/', login_required(views.ambiente_create), name='ambiente_create'),
    path('ambiente/<int:pk>/editar/', login_required(views.ambiente_update), name='ambiente_update'),
    path('ambiente/<int:pk>/excluir/', login_required(views.ambiente_delete), name='ambiente_delete'),

    # Ração
    path('racao/',login_required( views.racao_list), name='racao_list'),
    path('racao/novo/', login_required(views.racao_create), name='racao_create'),
    path('racao/<int:pk>/editar/', login_required(views.racao_update), name='racao_update'),
    path('racao/<int:pk>/excluir/', login_required(views.racao_delete), name='racao_delete'),

    # Água
    path('agua/', login_required(views.agua_list), name='agua_list'),
    path('agua/novo/', login_required(views.agua_create), name='agua_create'),
    path('agua/<int:pk>/editar/', login_required(views.agua_update), name='agua_update'),
    path('agua/<int:pk>/excluir/', login_required(views.agua_delete), name='agua_delete'),

    # Mortalidade
    path('mortalidade/', login_required(views.mortalidade_list), name='mortalidade_list'),
    path('mortalidade/novo/',login_required( views.mortalidade_create), name='mortalidade_create'),
    path('mortalidade/<int:pk>/editar/', login_required(views.mortalidade_update), name='mortalidade_update'),
    path('mortalidade/<int:pk>/excluir/', login_required(views.mortalidade_delete), name='mortalidade_delete'),

    # Pesagem
    path('pesagem/', login_required(views.pesagem_list), name='pesagem_list'),
    path('pesagem/novo/', login_required(views.pesagem_create), name='pesagem_create'),
    path('pesagem/<int:pk>/editar/', login_required(views.pesagem_update), name='pesagem_update'),
    path('pesagem/<int:pk>/excluir/', login_required(views.pesagem_delete), name='pesagem_delete'),

    # Tratamento
    path('tratamento/',login_required( views.tratamento_list), name='tratamento_list'),
    path('tratamento/novo/', login_required(views.tratamento_create), name='tratamento_create'),
    path('tratamento/<int:pk>/editar/', login_required(views.tratamento_update), name='tratamento_update'),
    path('tratamento/<int:pk>/excluir/', login_required(views.tratamento_delete), name='tratamento_delete'),

    # Vacinação
    path('vacinacao/', login_required(views.vacinacao_list), name='vacinacao_list'),
    path('vacinacao/novo/', login_required(views.vacinacao_create), name='vacinacao_create'),
    path('vacinacao/<int:pk>/editar/', login_required(views.vacinacao_update), name='vacinacao_update'),
    path('vacinacao/<int:pk>/excluir/', login_required(views.vacinacao_delete), name='vacinacao_delete'),

    # Evento
    path('evento/', login_required(views.evento_list), name='evento_list'),
    path('evento/novo/', login_required(views.evento_create), name='evento_create'),
    path('evento/<int:pk>/editar/',login_required( views.evento_update), name='evento_update'),
    path('evento/<int:pk>/excluir/', login_required(views.evento_delete), name='evento_delete'),

    # Alerta
    path('alerta/', login_required(views.alerta_list), name='alerta_list'),
    path('alerta/novo/',login_required(views.alerta_create), name='alerta_create'),
    path('alerta/<int:pk>/editar/', login_required(views.alerta_update), name='alerta_update'),
    path('alerta/<int:pk>/excluir/', login_required(views.alerta_delete), name='alerta_delete'),

    path('accounts/login/',  auth_views.LoginView.as_view(template_name="usuarios/login.html"),  name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'),                      name='logout'),

    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password...




]