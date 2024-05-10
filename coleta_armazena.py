import os
import time
import json
import argparse
import threading

# requirements.txt
import requests
import pandas as pd # type: ignore
import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore


def coleta(lat, lon, arquivo_saida, evento_conclusao_coleta):
    
    # 1. Consumir a API
    # Parâmetros para o consumo
    lang = "pt_br"
    metric = "metric"  
    api_key = "<sua_api_key>"
    url_acesso = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={metric}&lang={lang}&appid={api_key}'
    
    # Limite: 60 requisições/minuto ou 1.000.000 de requisições/mês
    # TODO: Aplicar um padrão de projeto que consiga realizar o máximo de requisições por dia.
    
    response = requests.get(url_acesso)
    data = response.json()
    
    # Selecionar os tipos de dados desejados
    if response.status_code == 200:
        print("|-----------1. Consumindo a API--------------|\n")
        print('Deu bom!\nRecolhendo os dados...\n')

        entidades = {
            'timestamp': data['dt'],
            'temperatura': data['main']['temp'],
            'umidade': data['main']['humidity'],
            'pressao': data['main']['pressure'],
            'direcao_vento': data['wind']['deg'],
            'velocidade_vento': data['wind']['speed']
        }
        
        # Visualizar os dados recolhidos
        df = pd.DataFrame(entidades, index=[0])
        print(df)
        print("\nTudo certo!")
        
        
        # Chamando a função de callback para armazenar os dados
        coleta_concluida(df, evento_conclusao_coleta)
    
    else:
        print('Erro:', response.status_code)
        print(response.text) 
        
    # 2. Parâmetros para o armazenamento local
    # print("\nIniciando o armazenamento...")
    # print("Criando os repositórios...")
    # if not os.path.exists('dados_brutos'):
    #     os.makedirs('dados_brutos')
    # 
    # caminho_json = os.path.join('dados_brutos', 'json')
    # caminho_csv = os.path.join('dados_brutos', 'csv')
    # 
    # 
    # if not os.path.exists(caminho_json):
    #     os.makedirs(caminho_json)
    # if not os.path.exists(caminho_csv):
    #     os.makedirs(caminho_csv)
    # 
    # # Armazenar localmente os dados em formato JSON e CSV
    # # Salvar em JSON
    # arquivo_json = os.path.join(caminho_json, 'response.json')
    # print("\nSalvando o arquivo JSON em", arquivo_json)
    # with open(arquivo_json, 'w') as arquivo_saida:
    #     json.dump(data, arquivo_saida, indent=4)
# 
    # # Salvar em CSV
    # arquivo_csv = os.path.join(caminho_csv, 'entidades.csv')
    # print("\nSalvando o arquivo CSV em", arquivo_csv)
    # df.to_csv(arquivo_csv, index=False)
    
    # Sinalizar a thread principal que a coleta foi concluída
    evento_conclusao_coleta.set()
    
    # Retornar o DataFrame criado
    return df
    
def armazena_mysql(df, evento_conclusao_coleta):
    # Espera até que o evento de conclusão da coleta seja acionado
    evento_conclusao_coleta.wait()
    
    # 3. Conectar e exportar os dados para o MySQL
    print("\n\n|-----------2. Iniciando o armazenamento remoto (MySQL)--------------|")
    
    # Delay pra conexão (15 segundos)
    time.sleep(10)
    
    # Conexão
    conexao = mysql.connector.connect(
        host="<seu_host>",
        user="<seu_usuario>",
        password="<sua_senha>",
        database="open_weather_map"
    )
    
    
    # Descrição da conexão
    db_info = conexao.get_server_info()
    print("\nConectado com sucesso ao servidor MySQL versão", db_info)
    # Cria o cursor e verifica a conexão
    cursor = conexao.cursor()
    cursor.execute("select database();")
    bd = cursor.fetchone()
    print("Conectado ao banco de dados ", bd)
    
    print("\nCriando a tabela 'current_weather'\n")
    # DDL: Criar uma tabela para o tipo de coleta        
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
    print("Tabela 'current_weather...' criada com sucesso!")
    
    # TODO: (i) Criar uma tabela para cada tipo de coleta (?)
    # criar_tabela = """
    # CREATE TABLE IF NOT EXISTS tipo_coleta (
    #     timestamp INT PRIMARY KEY,
    #     temperatura FLOAT,
    #     umidade INT,
    #     pressao INT,
    #     direcao_vento INT,
    #     velocidade_vento FLOAT
    # );"""
    # cursor.execute(criar_tabela)
    # print("\nTabela 'tipo_coleta' criada com sucesso!")
    
    
    # TODO: (ii) Verificar se os dados já existem.
    
    print("\nInserindo os dados...")
    # DML: Inserir os dados 
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
    
    # TODO: (iii) Atualizar os dados existentes.
    # DML: Atualizar os dados
    # query = "UPDATE current_weather SET temperatura = %s, umidade = %s, pressao = %s, direcao_vento = %s, velocidade_vento = %s WHERE timestamp = %s"
    # valores = (
        # float(row['temperatura']),
        # int(row['umidade']),
        # int(row['pressao']),
        # int(row['direcao_vento']),
        # float(row['velocidade_vento']),
        # int(row['timestamp'])
    # )
    # cursor.execute(query, valores)
    
    print("Commitando as alterações...\n")
    # Commit para salvar as alterações
    conexao.commit()
    print(cursor.rowcount, "registros inseridos na tabela.\n")
        
    print("|-----------Fim do serviço--------------|")
    if (conexao.is_connected()):
        # Fechar cursor e conexão
        cursor.close()
        conexao.close()
        print("|-----------Conexão finalizada--------------|")

# Função de callback para ser chamada quando a coleta estiver concluída
def coleta_concluida(df, evento_conclusao_coleta):
    # Armazena os dados no MySQL
    armazenamento_thread = threading.Thread(target=armazena_mysql, args=(df, evento_conclusao_coleta))
    armazenamento_thread.start()
    
    
# Módulo principal do programa
def main():
    
    # 0. Recolhe os parâmetros e verifica se foram passados os argumentos
    # Objeto para receber os argumentos da CLI
    parser = argparse.ArgumentParser(description="Coleta e armazena dados de uma estação meteorológica com base em coordenadas geográficas.")
    
    # Análise de argumentos
    ## Entrada
    parser.add_argument("--coord", nargs=2, metavar=('lat', 'long'), help="Latitude e longitude da estação meteorológica de interesse.")
    
    ## Nome do arquivo de saída
    #parser.add_argument("--out", metavar='arquivo_saida', help="Nome do arquivo de saída")
    
    args = parser.parse_args()
    if args.coord and args.out:
        
        # Evento para sinalizar a conclusão da coleta
        evento_conclusao_coleta = threading.Event()
        
        # Coleta de dados
        coleta_thread = threading.Thread(target=coleta, args=(args.coord[0], args.coord[1], args.out, evento_conclusao_coleta))
        
        coleta_thread.start()        
    else:
        print("Por favor, forneça as coordenadas de entrada e o nome do arquivo de saída.")

# Início do programa
if __name__ == "__main__":
    main()
