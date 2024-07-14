import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from weather_repository import WeatherRepository

# ---------------- Servico de coleta de dados climaticos ----------------
class OpenWeatherMapClient:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def get_weather_data(self, latitude, longitude):
        
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

# Transformação (ETL) | Após contato com a API Externa
def parse_weather_data(data):
    # TODO: Agendar jobs para coleta diária de dados via Apscheduler

    # Response: Formatação dos dados pra salvar no db_data
    return {
        'descricao_weather': data['weather'][0]['description'],
        'temperatura_atual': data['main']['temp'],
        'temperatura_max': data['main']['temp_max'],
        'temperatura_min': data['main']['temp_min'],
        'umidade': data['main']['humidity'],
        'velocidade_vento': data['wind']['speed'],
        'direcao_vento': data['wind']['deg'],
        'rajada_vento': data['wind'].get('gust', 0.0)
    }




