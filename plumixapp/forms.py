from django import forms
from .models import (
    Granja, Galpao, Lote, Ambiente, Racao, Agua,
    Mortalidade, Pesagem, Tratamento, Vacinacao, Evento, Alerta
)

# ---------- Utilidades embutidas ----------
STATUS_ATIVO_CHOICES = [
    ('ATIVO', 'ATIVO'),
    ('NÃO ATIVO', 'NÃO ATIVO'),
    ('VAZIO', 'VAZIO'),
]

class ChoiceBoolAdapterMixin:
    """
    Converte choices 'ATIVO'/'NÃO ATIVO'/'VAZIO' em boolean no cleaned_data.
    Use definindo bool_field_name = 'ativo_*'
    """
    bool_field_name = None

    def clean(self):
        cleaned = super().clean()
        if self.bool_field_name:
            val = cleaned.get(self.bool_field_name)
            if val == 'ATIVO':
                cleaned[self.bool_field_name] = True
            elif val == 'NÃO ATIVO':
                cleaned[self.bool_field_name] = False
            elif val == 'VAZIO':
                if self.instance and getattr(self.instance, self.bool_field_name, None) is not None:
                    cleaned[self.bool_field_name] = getattr(self.instance, self.bool_field_name)
                else:
                    cleaned[self.bool_field_name] = True  # fallback seguro p/ BooleanField sem null
        return cleaned


# ---------- GRANJA ----------
class GranjaForm(ChoiceBoolAdapterMixin, forms.ModelForm):
    bool_field_name = 'ativo_granja'

    class Meta:
        model = Granja
        # REMOVE 'cria_em_grnaj' (auto_now_add -> não editável)
        fields = ['id_granja', 'nome_granja','cnpj_granja','cidade_granja', 'uf_granja','ativo_granja']

    id_granja = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nome_granja = forms.CharField(label='Nome da granja:', widget=forms.TextInput(attrs={'class':'form-control'}))
    cnpj_granja = forms.CharField(label='CNPJ:', widget=forms.TextInput(attrs={'class':'form-control'}))
    cidade_granja = forms.CharField(label='Cidade:', widget=forms.TextInput(attrs={'class':'form-control'}))
    uf_granja = forms.CharField(label='UF:', widget=forms.TextInput(attrs={'class':'form-control'}))
    ativo_granja = forms.ChoiceField(
        label='Status:',
        choices=STATUS_ATIVO_CHOICES,
        widget=forms.Select(attrs={'class':'custom-select'}),
        initial='VAZIO',
    )


# ---------- GALPÃO ----------
class GalpaoForm(ChoiceBoolAdapterMixin, forms.ModelForm):
    bool_field_name = 'ativo_galpao'

    class Meta:
        model = Galpao
        # REMOVE 'cria_em_galpao'
        fields = ['id_galpao', 'nome_galpao', 'id_granja', 'codigo_galpao',
                  'cap_galpao', 'area_galpao', 'tipo_galpao', 'ativo_galpao']

    id_galpao = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nome_galpao = forms.CharField(label='Nome do galpão:', widget=forms.TextInput(attrs={'class':'form-control'}))
    id_granja = forms.ModelChoiceField(label='Granja:', queryset=Granja.objects.all(),
                                       widget=forms.Select(attrs={'class':'custom-select'}))
    codigo_galpao = forms.CharField(label='Código:', widget=forms.TextInput(attrs={'class':'form-control'}))
    cap_galpao = forms.IntegerField(label='Capacidade:', widget=forms.NumberInput(attrs={'class':'form-control','step':'1'}))
    area_galpao = forms.DecimalField(label='Área (m²):', max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    tipo_galpao = forms.CharField(label='Tipo:', widget=forms.TextInput(attrs={'class':'form-control'}))
    ativo_galpao = forms.ChoiceField(label='Status:', choices=STATUS_ATIVO_CHOICES,
                                     widget=forms.Select(attrs={'class':'custom-select'}), initial='VAZIO')


# ---------- LOTE ----------
class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        # REMOVE 'cria_em_lote'
        fields = ['id_lote','nome_lote','id_galpao','codigo_lote','linhagem_lote',
                  'd_entrada_lote','d_saida_lote','mot_saida_lote']

    id_lote = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nome_lote = forms.CharField(label='Nome do lote:', widget=forms.TextInput(attrs={'class':'form-control'}))
    id_galpao = forms.ModelChoiceField(label='Galpão:', queryset=Galpao.objects.all(),
                                       widget=forms.Select(attrs={'class':'custom-select'}))
    codigo_lote = forms.CharField(label='Código do lote:', widget=forms.TextInput(attrs={'class':'form-control'}))
    linhagem_lote = forms.CharField(label='Linhagem:', widget=forms.TextInput(attrs={'class':'form-control'}))
    d_entrada_lote = forms.DateField(label='Data de entrada:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    d_saida_lote = forms.DateField(label='Data de saída:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    mot_saida_lote = forms.CharField(label='Motivo da saída:', widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned = super().clean()
        de = cleaned.get('d_entrada_lote')
        ds = cleaned.get('d_saida_lote')
        if de and ds and ds < de:
            self.add_error('d_saida_lote', 'Data de saída não pode ser anterior à entrada.')
        return cleaned


# ---------- AMBIENTE ----------
class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        # REMOVE 'lido_em_ambiente'
        fields = ['id_ambiente', 'nome_leitura_ambiente', 'id_lote',
                  'temp_c_ambiente', 'co2_ambiente', 'nh3_ambiente',
                  'vel_ar_ambiente', 'sensor_ambiente']

    id_ambiente = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nome_leitura_ambiente = forms.CharField(label='Nome da leitura:', widget=forms.TextInput(attrs={'class':'form-control'}))
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    temp_c_ambiente = forms.DecimalField(label='Temperatura (°C):', max_digits=5, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    co2_ambiente = forms.IntegerField(label='CO₂ (ppm):', widget=forms.NumberInput(attrs={'class':'form-control','step':'1'}))
    nh3_ambiente = forms.IntegerField(label='NH₃ (ppm):', widget=forms.NumberInput(attrs={'class':'form-control','step':'1'}))
    vel_ar_ambiente = forms.DecimalField(label='Velocidade do ar (m/s):', max_digits=5, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    sensor_ambiente = forms.CharField(label='Sensor:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- RAÇÃO ----------
class RacaoForm(forms.ModelForm):
    class Meta:
        model = Racao
        fields = ['id_racao', 'id_lote', 'data_racao', 'kg_racao', 'fase_racao', 'obs_racao']

    id_racao = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_racao = forms.DateField(label='Data:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    kg_racao = forms.DecimalField(label='Quantidade (kg):', max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    fase_racao = forms.CharField(label='Fase da ração:', widget=forms.TextInput(attrs={'class':'form-control'}))
    obs_racao = forms.CharField(label='Observação:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- ÁGUA ----------
class AguaForm(forms.ModelForm):
    class Meta:
        model = Agua
        fields = ['id_agua', 'id_lote', 'data_agua', 'litro_agua', 'obs_agua']

    id_agua = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_agua = forms.DateField(label='Data:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    litro_agua = forms.DecimalField(label='Consumo (litros):', max_digits=12, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    obs_agua = forms.CharField(label='Observação:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- MORTALIDADE ----------
class MortalidadeForm(forms.ModelForm):
    class Meta:
        model = Mortalidade
        fields = ['id_mortalidade', 'id_lote', 'data_mortalidade', 'qtd_mortalidade', 'causa_mortalidade', 'obs_mortalidade']

    id_mortalidade = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_mortalidade = forms.DateField(label='Data:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    qtd_mortalidade = forms.IntegerField(label='Quantidade:', widget=forms.NumberInput(attrs={'class':'form-control','step':'1'}))
    causa_mortalidade = forms.CharField(label='Causa:', widget=forms.TextInput(attrs={'class':'form-control'}))
    obs_mortalidade = forms.CharField(label='Observação:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- PESAGEM ----------
class PesagemForm(forms.ModelForm):
    class Meta:
        model = Pesagem
        fields = ['id_pesagem','id_lote','data_pesagem','amostra_pesagem',
                  'pmedio_pesagem','cva_pesagem','obs_pesagem']

    id_pesagem = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_pesagem = forms.DateField(label='Data da pesagem:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    amostra_pesagem = forms.IntegerField(label='Nº amostras:', widget=forms.NumberInput(attrs={'class':'form-control','step':'1'}))
    pmedio_pesagem = forms.DecimalField(label='Peso médio (g):', max_digits=10, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class':'form-control','step':'0.01'}))
    cva_pesagem = forms.DecimalField(label='CV (%)', max_digits=6, decimal_places=3,
                                     widget=forms.NumberInput(attrs={'class':'form-control','step':'0.001'}))
    obs_pesagem = forms.CharField(label='Observação:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- TRATAMENTO ----------
class TratamentoForm(forms.ModelForm):
    class Meta:
        model = Tratamento
        fields = [
            'id_tratamento', 'id_lote', 'data_in_tratamento', 'data_fim_tratamento',
            'produto_tratamento', 'p_ativo_tratamento', 'via_tratamento',
            'dose_tratamento', 'motivo_tratamento'
        ]

    id_tratamento = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_in_tratamento = forms.DateField(label='Início:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    data_fim_tratamento = forms.DateField(label='Fim:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    produto_tratamento = forms.CharField(label='Produto:', widget=forms.TextInput(attrs={'class':'form-control'}))
    p_ativo_tratamento = forms.CharField(label='Princípio ativo:', widget=forms.TextInput(attrs={'class':'form-control'}))
    via_tratamento = forms.CharField(label='Via de administração:', widget=forms.TextInput(attrs={'class':'form-control'}))
    dose_tratamento = forms.CharField(label='Dose:', widget=forms.TextInput(attrs={'class':'form-control'}))
    motivo_tratamento = forms.CharField(label='Motivo:', widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned = super().clean()
        ini = cleaned.get('data_in_tratamento')
        fim = cleaned.get('data_fim_tratamento')
        if ini and fim and fim < ini:
            self.add_error('data_fim_tratamento', 'Data de fim não pode ser anterior ao início.')
        return cleaned


# ---------- VACINAÇÃO ----------
class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['id_vacinacao', 'id_lote', 'data_vacinacao', 'vacina_vacinacao', 'via_vacinacao', 'obs_vacinacao']

    id_vacinacao = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    data_vacinacao = forms.DateField(label='Data:', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    vacina_vacinacao = forms.CharField(label='Vacina:', widget=forms.TextInput(attrs={'class':'form-control'}))
    via_vacinacao = forms.CharField(label='Via de administração:', widget=forms.TextInput(attrs={'class':'form-control'}))
    obs_vacinacao = forms.CharField(label='Observação:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- EVENTO ----------
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        # REMOVE 'data_evento' (auto_now_add)
        fields = ['id_evento', 'id_lote', 'tipo_evento', 'descricao_evento']

    id_evento = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    tipo_evento = forms.CharField(label='Tipo:', widget=forms.TextInput(attrs={'class':'form-control'}))
    descricao_evento = forms.CharField(label='Descrição:', widget=forms.TextInput(attrs={'class':'form-control'}))


# ---------- ALERTA ----------
class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        # REMOVE 'data_alerta' e 'resolvido_em_alerta' (ambos não editáveis no seu model)
        fields = [
            'id_alerta', 'id_lote', 'severidade_alerta',
            'categoria_alerta', 'msg_alerta', 'resolvido_alerta'
        ]

    id_alerta = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_lote = forms.ModelChoiceField(label='Lote:', queryset=Lote.objects.all(),
                                     widget=forms.Select(attrs={'class':'custom-select'}))
    severidade_alerta = forms.CharField(label='Severidade:', widget=forms.TextInput(attrs={'class':'form-control'}))
    categoria_alerta = forms.CharField(label='Categoria:', widget=forms.TextInput(attrs={'class':'form-control'}))
    msg_alerta = forms.CharField(label='Mensagem:', widget=forms.TextInput(attrs={'class':'form-control'}))
    resolvido_alerta = forms.BooleanField(label='Resolvido?', required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
