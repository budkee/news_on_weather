import argparse
import random
import time
import MySQLdb
import requests
import pandas as pd
#from django.conf import settings
from .armazenaMySQL import ArmazenaMySQL

class ColetaAPI:
    
    def __init__(self, key, lat, lon):
        self.key = key
        self.lat = lat
        self.lon = lon
        self.lang = "pt_br"
        self.units = "metric"
        self.tipo = "forecast"
        self.url_template = 'https://api.openweathermap.org/data/2.5/{tipo}?lat={lat}&lon={lon}&units={units}&lang={lang}&appid={key}'

    def busca_dados(self, lat, lon, tipo):
        # Adapta a coleta de acordo com o tipo (Weather ou Forecast)
        url = self.url_template.format(tipo=tipo, lat=lat, lon=lon, units=self.units, lang=self.lang, key=self.key)
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Erro ao consumir API: {response.status_code}, {response.text}')
    
    def coleta_dados(self):
        
        data = self.busca_dados(self.lat, self.lon, self.tipo)
        
        # Forecast 
        ## Lista para armazenar as cidades e previsões
        cidades = []
        previsoes = []

        ## Recolha de acordo com o DDD
        ### Cidade    
        # Dados referente a uma localidade
        localidade = {
            'id_cidade': data['city']['id'],
            'cidade': data['city']['name'],
            'estado': "MS",
            'pais': "BR",
            'coord_lat': data['city']['coord']['lat'],
            'coord_lon': data['city']['coord']['lon'],
            'populacao': data['city']['population'],
            'timezone': data['city']['timezone'],
            'nascer_sol': data['city']['sunrise'],
            'baixar_sol': data['city']['sunset']
        }
        cidades.append(localidade)

        ### Previsão
        for previsao in data['list']:

            # Dados referente a uma previsão de 5 dias a cada 3 horas
            forecast = {
                'id_cidade': data['city']['id'],
                'data_hora_previsao': previsao['dt_txt'],
                'timestamp_previsao': previsao['dt'],
                'condicao': previsao['weather'][0]['main'],
                'descricao_condicao': previsao['weather'][0]['description'],
                'temperatura': previsao['main']['temp'],
                'max_temp': previsao['main']['temp_max'],
                'min_temp': previsao['main']['temp_min'],
                'sensacao': previsao['main']['feels_like'],
                'umidade': previsao['main']['humidity'],
                'pressao': previsao['main']['pressure'],
                'direcao_vento': previsao['wind']['deg'],
                'velocidade_vento': previsao['wind']['speed']
            }
        previsoes.append(forecast)

        df_localidades = pd.DataFrame(cidades)
        df_previsoes = pd.DataFrame(previsoes)
        
        return df_localidades, df_previsoes
    
def coleta_e_armazena_dados(api_key, lat, lon):

    coletor = ColetaAPI(api_key, lat, lon)
    armazenador = ArmazenaMySQL()  # Presumindo que não requer parâmetros para inicialização

    df_localidades = coletor.coleta_dados()
    armazenador.armazena_cidades(df_localidades)
    df_previsoes = coletor.coleta_dados() 
    armazenador.armazena_previsoes(df_previsoes)
    


def main():
    
    # Tratamento do input
    parser = argparse.ArgumentParser(description="Coleta e armazena dados de uma estação meteorológica com base em coordenadas geográficas.")
    parser.add_argument("--coord", nargs=2, metavar=('lat', 'lon'), required=True, help="Latitude e longitude da estação meteorológica de interesse.")
    parser.add_argument("--api_key", required=True, help="Chave de API do OpenWeatherMap.")
    
    # Armazena a localização e chave por parâmetro
    args = parser.parse_args()
    
    # Coleta e Armazenamento Remoto
    coleta_e_armazena_dados(args.api_key, float(args.coord[0]), float(args.coord[1]))
 
if __name__ == "__main__":
    main()
    
    # Input de exemplo: py coleta_armazena.py --coord <lat> <lon> --api_key <api>