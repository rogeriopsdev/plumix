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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    #path("login/", login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('usuarioapp.urls')),
# Granja
    path('granjas/', views.granja_list, name='granja_list'),
    path('granjas/novo/', views.granja_create, name='granja_create'),
    path('granjas/<int:pk>/editar/', views.granja_update, name='granja_update'),
    path('granjas/<int:pk>/excluir/', views.granja_delete, name='granja_delete'),

    # Galpão
    path('galpoes/', views.galpao_list, name='galpao_list'),
    path('galpoes/novo/', views.galpao_create, name='galpao_create'),
    path('galpoes/<int:pk>/editar/', views.galpao_update, name='galpao_update'),
    path('galpoes/<int:pk>/excluir/', views.galpao_delete, name='galpao_delete'),

    # Lote
    path('lotes/', views.lote_list, name='lote_list'),
    path('lotes/novo/', views.lote_create, name='lote_create'),
    path('lotes/<int:pk>/editar/', views.lote_update, name='lote_update'),
    path('lotes/<int:pk>/excluir/', views.lote_delete, name='lote_delete'),

    # Ambiente
    path('ambiente/', views.ambiente_list, name='ambiente_list'),
    path('ambiente/novo/', views.ambiente_create, name='ambiente_create'),
    path('ambiente/<int:pk>/editar/', views.ambiente_update, name='ambiente_update'),
    path('ambiente/<int:pk>/excluir/', views.ambiente_delete, name='ambiente_delete'),

    # Ração
    path('racao/', views.racao_list, name='racao_list'),
    path('racao/novo/', views.racao_create, name='racao_create'),
    path('racao/<int:pk>/editar/', views.racao_update, name='racao_update'),
    path('racao/<int:pk>/excluir/', views.racao_delete, name='racao_delete'),

    # Água
    path('agua/', views.agua_list, name='agua_list'),
    path('agua/novo/', views.agua_create, name='agua_create'),
    path('agua/<int:pk>/editar/', views.agua_update, name='agua_update'),
    path('agua/<int:pk>/excluir/', views.agua_delete, name='agua_delete'),

    # Mortalidade
    path('mortalidade/', views.mortalidade_list, name='mortalidade_list'),
    path('mortalidade/novo/', views.mortalidade_create, name='mortalidade_create'),
    path('mortalidade/<int:pk>/editar/', views.mortalidade_update, name='mortalidade_update'),
    path('mortalidade/<int:pk>/excluir/', views.mortalidade_delete, name='mortalidade_delete'),

    # Pesagem
    path('pesagem/', views.pesagem_list, name='pesagem_list'),
    path('pesagem/novo/', views.pesagem_create, name='pesagem_create'),
    path('pesagem/<int:pk>/editar/', views.pesagem_update, name='pesagem_update'),
    path('pesagem/<int:pk>/excluir/', views.pesagem_delete, name='pesagem_delete'),

    # Tratamento
    path('tratamento/', views.tratamento_list, name='tratamento_list'),
    path('tratamento/novo/', views.tratamento_create, name='tratamento_create'),
    path('tratamento/<int:pk>/editar/', views.tratamento_update, name='tratamento_update'),
    path('tratamento/<int:pk>/excluir/', views.tratamento_delete, name='tratamento_delete'),

    # Vacinação
    path('vacinacao/', views.vacinacao_list, name='vacinacao_list'),
    path('vacinacao/novo/', views.vacinacao_create, name='vacinacao_create'),
    path('vacinacao/<int:pk>/editar/', views.vacinacao_update, name='vacinacao_update'),
    path('vacinacao/<int:pk>/excluir/', views.vacinacao_delete, name='vacinacao_delete'),

    # Evento
    path('evento/', views.evento_list, name='evento_list'),
    path('evento/novo/', views.evento_create, name='evento_create'),
    path('evento/<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('evento/<int:pk>/excluir/', views.evento_delete, name='evento_delete'),

    # Alerta
    path('alerta/', views.alerta_list, name='alerta_list'),
    path('alerta/novo/', views.alerta_create, name='alerta_create'),
    path('alerta/<int:pk>/editar/', views.alerta_update, name='alerta_update'),
    path('alerta/<int:pk>/excluir/', views.alerta_delete, name='alerta_delete'),

]