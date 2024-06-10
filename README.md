# Sistema de coleta de dados climáticos

Criação de um script que realize a coleta e o armazenamento dos dados de interesse (ETL) a um banco de dados relacional (MySQL) a partir da [análise de modelagem do domínio do sistema](https://budkee.notion.site/Open-Weather-Map-3b2e4e5a58ec4898ad31f94c178ca2db?pvs=4).

## Endpoint de acesso | OpenWeatherMap

    https://api.openweathermap.org/data/2.5/weather?lat=-20.503313499221395&lon=-54.61106734104071&appid=768594c35657b6f2e8513d90431b7b02&units=metric

## Roteiro do script

1. Consumir a API
2. Armazenar no MySQL

### Inputs do serviço

    coleta_armazena.py --coord -20.45 -54.56 --out dados_coletados.json

### Visão do PhpMyAdmin

![visao_bd](./img/visao_bd.png)

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

### Documentação do Sistema

- [Análise e Modelagem do Sistema | Notion](https://budkee.notion.site/Open-Weather-Map-3b2e4e5a58ec4898ad31f94c178ca2db?pvs=4)
- [Componentes do Sistema | Notion](https://budkee.notion.site/Componentes-de-software-4c32db42b6584c9982c5c0b9314c788b?pvs=4)
- [Transformando Script de Coleta em Serviço de Coleta de dados | Notion](https://budkee.notion.site/Transformando-Script-de-Coleta-em-Servi-o-de-Coleta-de-dados-48c9f0be572849a7909e16e33daa3819)

### Tutoriais

- [Como conectar um script em Python a um banco de dados MySQL](https://youtu.be/FXlixv8Ieoc?si=5U9EPcKSe2ws1xOE)
- [Criar tabela em um banco MySQL com script em Python](https://youtu.be/yMqBfSl53MA?si=g9KJWvnqnD11OQAz)
- [Inserir dados em uma tabela MySQL com script em Python](https://youtu.be/HiK6OZjumew?si=--OkwhEDC8PEU1sv)
- [Realizar consulta a banco de dados MySQL usando o Python](https://youtu.be/GheUY9b_-ww?si=DqYoz97Biu3HfZAL)
- [COMO CRIAR UMA API REST DO ZERO COM DJANGO REST FRAMEWORK](https://www.youtube.com/watch?v=wtl8ZyCbTbg)
- [Como documentar uma API REST? - Swagger + Flask](https://youtu.be/wfVpAzhg6e0?si=_1ErjDIOUMrf4hnq)
- [Django Rest Framework em 30 minutos](https://youtu.be/gFsIGJR5R8I?si=cjeWDwtYMAaR2wwE)
- [PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [uritemplate](https://uritemplate.readthedocs.io/en/latest/)
- [Dockerizing a Django and MySQL Application: A Step-by-Step Guide | Medium](https://medium.com/@akshatgadodia/dockerizing-a-django-and-mysql-application-a-step-by-step-guide-d4ba181d3de5)

### Imagens Docker

- [Alpine | DockerHub](https://hub.docker.com/_/alpine)
- [MySQL | DockerHub](https://hub.docker.com/_/mysql)
- [PhpMyAdmin | DockerHub](https://hub.docker.com/_/phpmyadmin)

### Outros

- [Link desse repositório | GitHub](https://github.com/budkee/coleta_armazenamento_ddd)
- [Django REST Framework | Docs](https://www.django-rest-framework.org)
- [Previsão do tempo para 5 dias | OpenWeatherMap Docs](https://openweathermap.org/forecast5)
