from django.db import models

# Localidades
class Local(models.Model):

    id_cidade = models.IntegerField()
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=2)
    coord_lat = models.FloatField()
    coord_lon = models.FloatField()
    populacao = models.IntegerField()
    timezone = models.IntegerField()    
    nascer_sol = models.IntegerField()
    baixar_sol = models.IntegerField()
    
    def __str__(self):
        return self
    
# Previsões
class Previsao(models.Model):
    
    id_cidade = models.IntegerField()
    data_hora_previsao = models.CharField(max_length=50)
    timestamp_previsao = models.IntegerField()
    condicao = models.CharField(max_length=255)
    descricao_condicao = models.CharField(max_length=255)
    temperatura = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    sensacao = models.FloatField()
    umidade = models.IntegerField()
    pressao = models.IntegerField()
    direcao_vento = models.IntegerField()
    velocidade_vento = models.FloatField()
    
    def __str__(self):
        return self