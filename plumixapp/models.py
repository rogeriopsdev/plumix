from django.db import models

# Create your models here.
class Granja(models.Model):
    id_granja = models.AutoField(primary_key=True)
    nome_granja = models.CharField(max_length=255)
    cnpj_granja = models.CharField(max_length=255)
    cidade_granja = models.CharField(max_length=255)
    uf_granja = models.CharField(max_length=255)
    ativo_granja = models.BooleanField(default=True)
    cria_em_grnaj = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome_granja

class Galpao(models.Model):
    id_galpao = models.AutoField(primary_key=True)
    nome_galpao = models.CharField(max_length=255)
    id_granja = models.ForeignKey('Granja', on_delete=models.CASCADE)
    codigo_galpao = models.CharField(max_length=255)
    cap_galpao = models.IntegerField(default=0)
    area_galpao = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_galpao = models.CharField(max_length=255)
    ativo_galpao = models.BooleanField(default=True)
    cria_em_galpao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome_galpao

class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    nome_lote = models.CharField(max_length=255)
    id_galpao = models.ForeignKey('Galpao', on_delete=models.CASCADE)
    codigo_lote = models.CharField(max_length=255)
    linhagem_lote = models.CharField(max_length=255)
    d_entrada_lote = models.DateField()
    d_saida_lote = models.DateField()
    mot_saida_lote = models.CharField(max_length=255)
    cria_em_lote = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome_lote


class Ambiente(models.Model):
    id_ambiente = models.AutoField(primary_key=True)
    nome_leitura_ambiente = models.CharField(max_length=255)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    lido_em_ambiente = models.DateTimeField(auto_now_add=True)
    temp_c_ambiente = models.DecimalField(max_digits=5, decimal_places=2)
    co2_ambiente = models.IntegerField(default=0)
    nh3_ambiente = models.IntegerField(default=0)
    vel_ar_ambiente = models.DecimalField(max_digits=5, decimal_places=2)
    sensor_ambiente = models.CharField(max_length=255)
    def __str__(self):
        return self.nome_leitura_ambiente

class Racao(models.Model):
    id_racao = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_racao = models.DateField()
    kg_racao = models.DecimalField(max_digits=10, decimal_places=2)
    fase_racao = models.CharField(max_length=255)
    obs_racao = models.CharField(max_length=255)
    def __str__(self):
        return self.fase_racao

class Agua(models.Model):
    id_agua = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_agua = models.DateField()
    litro_agua = models.DecimalField(max_digits=12, decimal_places=2)
    obs_agua = models.CharField(max_length=255)
    def __str__(self):
        return self.obs_agua


class Mortalidade(models.Model):
    id_mortalidade = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_mortalidade = models.DateField()
    qtd_mortalidade = models.IntegerField(default=0)
    causa_mortalidade = models.CharField(max_length=255)
    obs_mortalidade = models.CharField(max_length=255)
    def __str__(self):
        return self.obs_mortalidade

class Pesagem(models.Model):
    id_pesagem = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_pesagem = models.DateField()
    amostra_pesagem = models.IntegerField(default=0)
    pmedio_pesagem = models.DecimalField(max_digits=10, decimal_places=2)
    cva_pesagem = models.DecimalField(max_digits=6, decimal_places=3)
    obs_pesagem = models.CharField(max_length=255)

    def __str__(self):

        return self.obs_pesagem

class Tratamento(models.Model):
    id_tratamento = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_in_tratamento = models.DateField()
    data_fim_tratamento = models.DateField()
    produto_tratamento = models.CharField(max_length=255)
    p_ativo_tratamento = models.CharField(max_length=255)
    via_tratamento = models.CharField(max_length=255)
    dose_tratamento = models.CharField(max_length=255)
    motivo_tratamento = models.CharField(max_length=255)

    def __str__(self):

        return self.motivo_tratamento

class Vacinacao(models.Model):
    id_vacinacao = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_vacinacao = models.DateField()
    vacina_vacinacao = models.CharField(max_length=255)
    via_vacinacao = models.CharField(max_length=255)
    obs_vacinacao = models.CharField(max_length=255)

    def __str__(self):
        return self.obs_vacinacao

class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_evento = models.DateTimeField(auto_now_add=True)
    tipo_evento = models.CharField(max_length=255)
    descricao_evento = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao_evento

class Alerta(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE)
    data_alerta = models.DateTimeField(auto_now_add=True)
    severidade_alerta = models.CharField(max_length=255)
    categoria_alerta = models.CharField(max_length=255)
    msg_alerta = models.CharField(max_length=255)
    resolvido_alerta = models.BooleanField(default=True)
    resolvido_em_alerta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.msg_alerta


