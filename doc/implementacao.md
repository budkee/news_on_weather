# Como implementar?

## Pré-requisitos

- Docker

## Passos

1. Acesse, via CLI, o diretório que contenha o compose `api_flask_compose.yml` e digite `docker compose -f api_flask_compose.yml up --build`, caso queira ver o log, ou `docker compose -f api_flask_compose.yml up -d --build` caso contrário. O parâmetro `--build` constrói a imagem dos serviços antes de subir e o `-f` passa o nome do arquivo.

2. Acesse, no seu navegador de preferência, http://localhost:6767/{endpoint_de_interesse}.

### Endpoints

#### Weather
- http://localhost:6767/weather/ | GET
- http://localhost:6767/weather/collect | POST
- http://localhost:6767/weather/data | GET
- http://localhost:6767/weather/latest_data | GET

#### Newsletter
- http://localhost:6767/newsletter/ | POST
- http://localhost:6767/newsletter/register | POST
- http://localhost:6767/newsletter/unsubscribe | POST
- http://localhost:6767/newsletter/send_email | POST

