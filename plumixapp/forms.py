from cProfile import label
from symtable import Class

from plumixapp.models import *
from django import forms
from django.db.models import fields


class GranjaForm(forms.ModelForm):
    ATIVO =[
        ('ATIVO', 'ATIVO'),
        ('NÃO ATIVO','NÃO ATIVO'),
        ('VAZIO','VAZIO'),
    ]

    class Meta:
        model=Granja
        fields =['id_granja', 'nome_granja','cnpj_granja','cidade_granja', 'uf_granja','ativo_granja', 'criado_em_granja']

    id_granja = forms.IntegerField(label='ID:',widget=forms.HiddenInput())
    nome_granja = forms.CharField(label='Nome da granja:',widget=forms.TextInput(attrs={'class':'form-control'}))
    cnpj_granja = forms.CharField(label='CNPJ:',widget=forms.TextInput(attrs={'class':'form-control'}))
    cidade_granja = forms.CharField(label='Cidade',widget=forms.TextInput(attrs={'class':'form-control'}))
    uf_granja = forms.CharField(label='UF',widget=forms.TextInput(attrs={'class':'form-control'}))
    ativo_granja = forms.ChoiceField(
        label='Status:',
        choices= ATIVO,
        widget=forms.Select(attrs={'class':'custom-select'}),
        initial='VAZIO',
    )
    criado_em_granja = forms.DateTimeField(label='Criado em:',widget=forms.HiddenInput())

class GalpaoForm(forms.ModelForm):
    ATIVO = [
        ('ATIVO', 'ATIVO'),
        ('NÃO ATIVO', 'NÃO ATIVO'),
        ('VAZIO', 'VAZIO'),
    ]
    class Meta:
        model=Galpao
        fields=['id_galpao','nome_galpao','id_granja','codigo_galpao','area_galpao','tipo_galpao','ativo_galpao','criado_em_galpao']

    id_galpao = forms.IntegerField(widget=forms.HiddenInput())
    nome_galpao = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    id_granja = forms.IntegerField(widget=forms.HiddenInput())
