# Dockerfile | Serviço de Coleta e Armazenamento Remoto (linux:MySQL)
FROM python:3.10-alpine

# Gestão das dependências do linux
RUN apk update \
    && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        python3-dev \
        libxml2-dev \
        libxslt-dev \
        postgresql-dev \
        mariadb-dev \
        zlib-dev \
        jpeg-dev \
        zlib \
        zlib-dev \
        build-base \
        libjpeg \
        jpeg-dev \
        zlib-dev \
        zsh \
        wget \
        git \
        vim \
        tree \
        sudo \
        shadow \
        python3 \
        mysql-client \
    && rm -rf /var/cache/apk/* 

# Adiciona um usuário não-root
RUN adduser -D sirius && \
    addgroup sirius wheel && \
    echo "sirius ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/sirius && \
    chmod 0440 /etc/sudoers.d/sirius && \
    chsh -s /bin/zsh sirius
    
COPY .zshrc /home/sirius/.zshrc

# Variáveis do Ambiente 
ENV PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH
ENV PATH=$HOME/home/sirius/.local/bin:$PATH
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/mysql -lmysqlclient"
## Define a codificação padrão do Python
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
## Diretório onde os plugins Zsh serão instalados
ENV ZSH_CUSTOM=/home/sirius/.oh-my-zsh/custom
ENV ZSH="$HOME/.oh-my-zsh"

RUN sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting && \
    git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions 
    # source ~/.zshrc

# Define o diretório de trabalho padrão
WORKDIR /app

# Define o Zsh como shell padrão
SHELL ["/bin/zsh", "-c"]

# Copia os arquivos do código-fonte para o contêiner
COPY . /app

# Ajustar as permissões de /app
RUN chmod -R 755 /app && \ 
    chown -R sirius:sirius /app

# Define o usuário padrão
USER sirius

# Instalação dos requisitos do sistema
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 


EXPOSE 8000
