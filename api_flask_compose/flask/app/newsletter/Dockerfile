FROM python:3.10-alpine3.20

# No / da imagem
RUN pip install --upgrade pip

# TODO: criar um usuário para melhoria da segurança

# Prevent Python from writing .pyc files and enable unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# No diretório da aplicação/container
WORKDIR /app

# Copiar os arquivos de interesse
COPY . /app
COPY entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /requirements.txt

# Requisitos do sistema
RUN pip install -r requirements.txt

# Ensure the entrypoint script has execute permissions
RUN chmod +x /entrypoint.sh

# Comando ao inicializar o container
ENTRYPOINT [ "sh", "/entrypoint.sh" ]