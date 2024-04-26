import time
import json
import argparse
import threading

# requirements.txt
import requests
import pandas as pd # type: ignore
import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore


# 1. Consumir a API
def coleta(lat, lon, arquivo_saida, evento_conclusao_coleta):
    # Parâmetros para o consumo
    lang = "pt_br"
    metric = "metric"  
    api_key = "eaf6771e887f40128a529e15f989718f"
    url_acesso = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={metric}&lang={lang}&appid={api_key}'
    
    # Limite: 60 requisições/minuto ou 1.000.000 de requisições/mês
    # TODO: Aplicar um padrão de projeto que consiga realizar o máximo de requisições por dia.
    response = requests.get(url_acesso)
    data = response.json()
    
    # Verifique o código de status da resposta
    if response.status_code == 200:
        print('Deu bom!')
        print('Você está trabalhando com: ', type(data))
        df = pd.DataFrame(data)
        print(df) 
    
    else:
        print('Erro:', response.status_code)
        print(response.text) 
        
    #print("!\nSalvando o arquivo e armazenando no MySQL...\n")
    
    # 2. Armazenar em um arquivo .json
    with open(arquivo_saida, 'w') as aS:
        json.dump(data, aS, indent=4)
    
    # Sinalizar que a coleta foi concluída
    evento_conclusao_coleta.set()
    
# 3. Conectar e exportar os dados para o MySQL
def armazena_mysql(arquivo_saida, evento_conclusao_coleta):
    # Espera até que o evento de conclusão da coleta seja acionado
    evento_conclusao_coleta.wait()
    
    # Delay pra conexão (15 segundos)
    #time.sleep(15)
    
    # Ler o arquivo JSON
    with open(arquivo_saida, 'r') as dc:
        data = json.load(dc)
    
    # Conexão
    conexao = mysql.connector.connect(
        host="mysql",
        user="siriusb",
        password="sirius",
        database="open_weather_map"
    )
    
    
    # Descrição da conexão
    db_info = conexao.get_server_info()
    print("\n\nConectado com sucesso ao servidor MySQL versão", db_info)
    # Cria o cursor e verifica a conexão
    cursor = conexao.cursor()
    cursor.execute("select database();")
    bd = cursor.fetchone()
    print("Conectado ao banco de dados ", bd)
    
    # DDL: Criar uma tabela para o tipo de coleta        
    criar_tabela = """
    CREATE TABLE IF NOT EXISTS current_weather (
        timestamp TIMESTAMP PRIMARY KEY,
        temperatura FLOAT,
        umidade INT,
        pressao_atmosferica INT,
        direcao_vento FLOAT,
        velocidade_vento FLOAT
    );"""
    cursor.execute(criar_tabela)
    print("Tabela 'current_weather' criada com sucesso!")
    #print(cursor.fetchone())
    
    # DML: Inserir os dados 
    #query = "INSERT INTO current_weather (timestamp, temperatura, umidade, pressao_atmosferica, direcao_vento, velocidade_vento) VALUES (%d, %f, %d, %d, %d, %f)"
#    valores = (
#        data['dt'], 
#        data['main']['temp'], 
#        data['main']['humidity'], 
#        data['main']['pressure'], 
#        data['wind']['deg'], 
#        data['wind']['speed']
#    )
    
    #print(query)
    #print(valores)
    #cursor.execute(query, valores)
    
    

    # Commit para salvar as alterações
    conexao.commit()
    #print(cursor.rowcount, "registros inseridos na tabela.")
        
        
    if (conexao.is_connected()):
        # Fechar cursor e conexão
        cursor.close()
        conexao.close()
        print("Conexão finalizada.")


# Módulo principal do programa
def main():
    
    # Recebe os argumentos da CLI
    parser = argparse.ArgumentParser(description="Coleta e armazena dados de uma estação meteorológica com base em coordenadas geográficas.")
    
    ## Entrada
    parser.add_argument("--coord", nargs=2, metavar=('lat', 'long'), type=float, help="Latitude e longitude da estação meteorológica de interesse.")
    
    ## Nome do arquivo de saída
    parser.add_argument("--out", metavar='arquivo_saida', help="Arquivo de saída em JSON")
    
    # Recolhe os parâmetros e verifica se foram passados os argumentos
    args = parser.parse_args()
    if args.coord and args.out:
        
        # Evento para sinalizar a conclusão da coleta
        evento_conclusao_coleta = threading.Event()
        
        # Thread 1: Coleta de dados
        # coleta(args.coord[0], args.coord[1], args.out)
        # Iniciar a coleta e o armazenamento em threads separadas
        coleta_thread = threading.Thread(target=coleta, args=(args.coord[0], args.coord[1], args.out, evento_conclusao_coleta))
        coleta_thread.start()
        
        # Thread 2: Armazena no MySQL
        # armazena_mysql(args.out)
        #armazenamento_thread = threading.Thread(target=armazena_mysql, args=(args.out,evento_conclusao_coleta))
        #armazenamento_thread.start()
    else:
        print("Por favor, forneça as coordenadas de entrada e o nome do arquivo de saída.")

# Início do programa
if __name__ == "__main__":
    main()
