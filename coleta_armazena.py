import argparse
import requests
import pandas as pd
import mysql.connector
import time
import random

class SingletonMeta(type):
    """
    Implementação thread-safe de Singleton.
    """
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class consumo_API(metaclass=SingletonMeta):
    
    def __init__(self):
        self.api_key = "<sua_api_key>"
        self.lang = "pt_br"
        self.metric = "metric"
        self.url_template = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&lang={lang}&appid={api_key}'

    def busca_dados_meteorologicos(self, lat, lon):
        url = self.url_template.format(lat=lat, lon=lon, units=self.metric, lang=self.lang, api_key=self.api_key)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Erro ao consumir API: {response.status_code}, {response.text}')

class coleta_dados:
    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.api_client = consumo_API()

    def coleta_dados(self):
        data = self.api_client.busca_dados_meteorologicos(self.lat, self.lon)
        entities = {
            'timestamp': data['dt'],
            'temperatura': data['main']['temp'],
            'umidade': data['main']['humidity'],
            'pressao': data['main']['pressure'],
            'direcao_vento': data['wind']['deg'],
            'velocidade_vento': data['wind']['speed']
        }
        df = pd.DataFrame([entities])
        print(df)
        return df

class armazena_mysql(metaclass=SingletonMeta):
    
    def __init__(self):
        self.conexao = None

    def connect(self):
        if self.conexao is None or not self.conexao.is_connected(): 
            self.conexao = mysql.connector.connect(
                host="<seu_host>",
                user="<seu_usuario>",
                password="<sua_senha>",
                database="open_weather_map"
            )
            if not self.conexao.is_connected():
                raise Exception("Falha na conexão com o banco de dados.")
            print(f"Conectado ao servidor MySQL versão {self.conexao.get_server_info()}")

    def close(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()

    def armazena_dados(self, df):
        if not self.conexao or not self.conexao.is_connected():
            raise Exception("Não há conexão ativa com o banco de dados.")

        cursor = self.conexao.cursor()
        cursor.execute("select database();")
        print(f"Conectado ao banco de dados {cursor.fetchone()}")

        criar_tabela = """
        CREATE TABLE IF NOT EXISTS current_weather (
            timestamp INT PRIMARY KEY,
            temperatura FLOAT,
            umidade INT,
            pressao INT,
            direcao_vento INT,
            velocidade_vento FLOAT
        );"""
        cursor.execute(criar_tabela)

        for _, row in df.iterrows():
            query = "INSERT INTO current_weather (timestamp, temperatura, umidade, pressao, direcao_vento, velocidade_vento) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (
                int(row['timestamp']),
                float(row['temperatura']),
                int(row['umidade']),
                int(row['pressao']),
                int(row['direcao_vento']),
                float(row['velocidade_vento'])
            )
            cursor.execute(query, valores)

        self.conexao.commit()
        print(f"{cursor.rowcount} registros inseridos na tabela.")
        cursor.close()

def main():
    
    parser = argparse.ArgumentParser(description="Coleta e armazena dados de uma estação meteorológica com base em coordenadas geográficas.")
    parser.add_argument("--coord", nargs=2, metavar=('lat', 'lon'), required=True, help="Latitude e longitude da estação meteorológica de interesse.")
    args = parser.parse_args()
    
    coletor = coleta_dados(args.coord[0], args.coord[1])
    armazenamento = armazena_mysql()
    armazenamento.connect()

    try:
        while True:
            df = coletor.coleta_dados()
            armazenamento.armazena_dados(df)
            
            sleep_time = random.uniform(1, 60 / 60)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("Coleta interrompida pelo usuário.")
    finally:
        armazenamento.close()

if __name__ == "__main__":
    main()
