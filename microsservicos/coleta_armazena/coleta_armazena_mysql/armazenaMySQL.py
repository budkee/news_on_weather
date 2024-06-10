import MySQLdb
# from django.http import JsonResponse

class ArmazenaMySQL:
    
    def __init__(self):
        self.conexao = None

    def connect(self):
        try:
            if self.conexao is None or not self._is_connection_open():
                self.conexao = MySQLdb.connect(
                    host="db",
                    user="root",
                    password="<your-rootpass>",
                    database="db_coleta_armazena"
                )
                print(f"Conectado ao servidor MySQL versão {self.conexao.get_server_info()}")
        except MySQLdb.Error as e:
            raise Exception("Falha na conexão com o banco de dados.")

    def _is_connection_open(self):
        try:
            self.conexao.ping() # type: ignore
            return True
        except MySQLdb.Error:
            return False
    
    def close(self):
        if self.conexao:
            try:
                self.conexao.close()
                print('Conexão com o banco de dados fechada.')
            except MySQLdb.Error as e:
                print(f'Erro ao fechar a conexão: {e}')

    def fetch_localidades(self):
        self.connect()
        cursor = self.conexao.cursor(MySQLdb.cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM cidades")
        localidades = cursor.fetchall()
        cursor.close()
        self.close()
        return localidades

    def fetch_previsoes(self):
        self.connect()
        cursor = self.conexao.cursor(MySQLdb.cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM previsoes")
        previsoes = cursor.fetchall()
        cursor.close()
        self.close()
        return previsoes

    def armazena_cidades(self, df_cidades):
        
        if not self.conexao or not self._is_connection_open():
            raise Exception("Não há conexão ativa com o banco de dados.\nTentando conectar...")
            self.connect()

        cursor = self.conexao.cursor()
        criar_tabela_cidades = """
        CREATE TABLE IF NOT EXISTS cidades (
            id_cidade INT PRIMARY KEY,
            cidade VARCHAR(50),
            estado VARCHAR(2),
            pais VARCHAR(2),
            coord_lat FLOAT,
            coord_lon FLOAT,
            populacao INT,
            timezone INT,
            nascer_sol INT,
            baixar_sol INT
        );
        """
        cursor.execute(criar_tabela_cidades)

        for _, row in df_cidades.iterrows():
            query = """
            INSERT INTO cidades (id_cidade, cidade, estado, pais, coord_lat, coord_lon, populacao, timezone, nascer_sol, baixar_sol) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cidade=VALUES(cidade), estado=VALUES(estado), pais=VALUES(pais), coord_lat=VALUES(coord_lat), coord_lon=VALUES(coord_lon), populacao=VALUES(populacao), timezone=VALUES(timezone), nascer_sol=VALUES(nascer_sol), baixar_sol=VALUES(baixar_sol);
            """
            valores = (
                int(row['id_cidade']),
                row['cidade'],
                row['estado'],
                row['pais'],
                float(row['coord_lat']),
                float(row['coord_lon']),
                int(row['populacao']),
                int(row['timezone']),
                int(row['nascer_sol']),
                int(row['baixar_sol'])
            )
            cursor.execute(query, valores)

        self.conexao.commit()
        print(f"{cursor.rowcount} registros inseridos/atualizados na tabela cidades.")
        cursor.close()

    def armazena_previsoes(self, df_previsoes):
        if not self.conexao or not self._is_connection_open():
            raise Exception("Não há conexão ativa com o banco de dados.\nTentando conectar...")
            self.connect()

        cursor = self.conexao.cursor()
        criar_tabela_previsoes = """
        CREATE TABLE IF NOT EXISTS previsoes (
            id_cidade INT,
            data_hora_previsao DATETIME,
            timestamp_previsao INT,
            condicao VARCHAR(255),
            descricao_condicao VARCHAR(255),
            temperatura FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            sensacao FLOAT,
            umidade INT,
            pressao INT,
            direcao_vento INT,
            velocidade_vento FLOAT,
            PRIMARY KEY (id_cidade, timestamp_previsao)
        );
        """
        cursor.execute(criar_tabela_previsoes)

        for _, row in df_previsoes.iterrows():
            query = """
            INSERT INTO previsoes (id_cidade, data_hora_previsao, timestamp_previsao, condicao, descricao_condicao, temperatura, max_temp, min_temp, sensacao, umidade, pressao, direcao_vento, velocidade_vento) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE data_hora_previsao=VALUES(data_hora_previsao), condicao=VALUES(condicao), descricao_condicao=VALUES(descricao_condicao), temperatura=VALUES(temperatura), max_temp=VALUES(max_temp), min_temp=VALUES(min_temp), sensacao=VALUES(sensacao), umidade=VALUES(umidade), pressao=VALUES(pressao), direcao_vento=VALUES(direcao_vento), velocidade_vento=VALUES(velocidade_vento);
            """
            valores = (
                int(row['id_cidade']),
                row['data_hora_previsao'],
                int(row['timestamp_previsao']),
                row['condicao'],
                row['descricao_condicao'],
                float(row['temperatura']),
                float(row['max_temp']),
                float(row['min_temp']),
                float(row['sensacao']),
                int(row['umidade']),
                int(row['pressao']),
                int(row['direcao_vento']),
                float(row['velocidade_vento'])
            )
            cursor.execute(query, valores)

        self.conexao.commit()
        print(f"{cursor.rowcount} registros inseridos/atualizados na tabela previsoes.")
        cursor.close()
