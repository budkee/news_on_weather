# Mapeamento Relacional | Coleta OpenWeatherMap

## Entidades e Relacionamentos

- Localidades(*id_cidade*: int, cidade: varchar(30), estado: char(2), pais: char(2), coord_lat: float, coord_lon: float, populacao: int, timezone: int, nascer_sol: timestamp, baixar_sol: timestamp)

- Previsao(*id_cidade*: int, data_hora_previsao: varchar(50), timestamp_previsao: int, condicao: varchar(255), descricao_condicao: varchar(255), temperatura: float, max_temp: float, min_temp: float, sensacao: float, umidade: int, pressao: int, direcao_vento: int, velocidade_vento: float)
