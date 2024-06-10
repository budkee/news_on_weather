# Use a imagem base do Ubuntu Minimal
FROM ubuntu:22.04 AS base

# Configuração não interativa durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza o índice de pacotes e instalações do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-distutils \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o Python 3 como padrão
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3 1

# Define a codificação padrão do Python
ENV PYTHONIOENCODING=UTF-8

# Define o diretório de trabalho padrão
WORKDIR /app

# Copia os arquivos do código-fonte para o contêiner
COPY . /app

# Define a variável de ambiente PATH para incluir o diretório .local/bin do usuário
ENV PATH=/root/.local/bin:$PATH

# Instala o pipenv globalmente
RUN python3.10 -m pip install --upgrade pip pipenv

# Define o comando padrão a ser executado quando o contêiner for iniciado
CMD ["/bin/bash"]
