# Desenvolvimento inicial do sistema de coleta de dados climáticos

- [Projeto de software](https://budkee.notion.site/Open-Weather-Map-3b2e4e5a58ec4898ad31f94c178ca2db?pvs=4)

## Objetivo

Criação de um script que realize a coleta e o armazenamento dos dados em um banco de dados relacional.

## Pontos a serem considerados

- A API da OpenWeatherMap fornece 2 opções de envio do pacote: `json` e `xml`.
- O MySQL, banco de dados escolhido, não lê dados em `json` para importação via GUI.

## Roteiro do script

1. Consumir a API
2. Armazenar em um arquivo .json
3. Conectar e exportar os dados para o MySQL

### Inputs do usuário

    coleta_armazena.py --coord -20.45 -54.56 --out dados_coletados.json

### Outputs esperado

- O arquivo em json da coleta no repositório que foi executado;
- Um texto dizendo se os dados foram ou não salvos no MySQL corretamente;

### Parâmetros do consumo

- unidade de medida utilizada: `metric`
- latitude: `lat`
- longitude: `long`
- linguagem: `pt-br`

## Dados de interesse | Current Weather

- temperatura: `main.temp`
- umidade: `main.humidity`
- pressão atmosférica: `pressure`
- direção do vento: `wind.deg`
- velocidade do vento: `wind.speed`
- timestamp: `dt`

## Links e Referências

- [OpenWeatherMap | Docs](https://openweathermap.org/current)

