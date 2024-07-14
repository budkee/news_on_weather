# Passando a aplicação Flask para Django

## Passos

1. Criar o compose contendo os seguintes componentes:
    a. Servidor com python:3.10;
    b. Servidor do postgresql:latest;
    c. Interface do pgadmin4:8.9;
    d. Servidor Web com nginx:latest;

2. Configurar o ambiente de cada componente.

### Servidor com python:3.10

- [Dependências | `pip install -r requirements.txt`]()
- [Dockerfile | `docker compose -f microsservicos_tads.yml up -d --build`](./Dockerfile)
- [Comandos ao iniciar o servidor | `python`](entrypoint.sh)
- [Variáveis de ambiente | `os.getenv()`](env-template)

#### Dependências | `pip`

Ao construir a imagem `build` no Dockerfile, todas as dependências declaradas no arquivo `requirements.txt` serão instaladas no servidor, não sendo necessário criar um ambiente de desenvolvimento virtual (venv), apesar de ser recomendado:

    > $ WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

#### Dockerfile | `docker compose -f microsservicos_tads.yml up -d --build`

Cada pasta do diretório da aplicação representa o contexto de `build` de um componente, ou serviço, que foi declarado no arquivo do [compose](microsservicos_tads.yml). Assim, cada variável de ambiente deverá ser declarada dentro do diretório do componente pelo arquivo `.env`. O parâmetro `-f` representa o nome do arquivo que contém o compose, que neste caso é `microsservicos_tads.yml`. O `-d` solicita que seja executado em segundo plano e o `--build` realiza a construção da imagem antes de subir a composição. Todas as vezes que for alterado alguma coisa no aquivo de compose ou qualquer uma de suas dependências subjacentes(arquivos de configuração, Dockefile, requirements.txt), uma nova imagem deverá ser construída.

#### Comandos ao iniciar o servidor | `python`

Ao executar o comando `docker compose up -d --build`, o [arquivo de entrada](./django/entrypoint.sh) será o responsável por iniciar o servidor da aplicação django, realizando a migração dos modelos ao banco de dados e deixando o servidor aberto para acesso remoto via `gunicorn`.

#### Comandos ao começar um novo projeto e aplicações Django

    > $ django-admin startproject <nome> <diretório>

> $ django-admin startproject api .
> $ python manage.py migrate
> $ python manage.py createsuperuser

- Verifique se a interface e o usuário estão configurados corretamente:

> $ gunicorn api.wsgi:application --bind 0.0.0.0:8000
> ou
> $ ./manage.py runserver 0.0.0.0:8000

- Começar uma nova aplicação:

> $ ./manage.py startapp data

### Servidor do postgresql:latest

- Ajustar as variáveis para os bancos de dados `db_data` e `db_newsletter` em `settings.py` na raiz do projeto `api.settings`.

- Criar os arquivos para rotear os dados aos seus respectivos bancos de dados: `data/router.py` e `newsletter/router.py`.

- Criar tabelas para os aplicativos/serviços sem fazer as migrações.

> $ ./manage.py migrate  --run-syncdb

- Comando para realizar as criações no banco de dados de acordo com o serviço específico.

> $ ./manage.py migrate
> $ ./manage.py migrate --database=db_data data
> $ ./manage.py migrate --database=db_newsletter newsletter

- Comando para criar novas migrações para apps (scripts em SQL que ficam armazenados em `migrations/`).

> $ ./manage.py makemigrations app_label
> $ ./manage.py makemigrations --dry-run app_label          # Verifica quais são as mudanças a serem executadas antes de executar

