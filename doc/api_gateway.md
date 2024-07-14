# Configurando um proxy reverso para cada serviço | API Gateway

De um modo geral, podemos entender que cada servidor (weather_api e newsletter_api) será um serviço no composer e o ngnix fará o proxy para o respectivo serviço. 

Este documento serve como guia para replicação da API Gateway para este projeto e outros futuros.

- [Como verificar?](implementacao.md)

## Roadmap da implantação

0. Adicionar a lib do `gunicorn` em cada serviço via `requirements.txt`.
1. Construir a imagem para os serviços.
2. Testar a aplicação com o gunicorn
3. Configurar o caminho `location` de cada endpoint no arquivo de configurações do nginx `conf.d/nginx.conf`.

### Construir a imagem para os serviços.

1.1. Após configurar o Dockerfile, execute `docker build -t weather_api .` dentro do diretório do serviço. Faça o mesmo para o serviço de newsletter: `docker build -t newsletter_api .`
<!-- 1.2. TODO: Subir para o docker hub. -->

### Testar a aplicação com o gunicorn

2.1. Configurar o `entrypoint.sh` de cada serviço, adicionando o comando `gunicorn -w 4 --bind 0.0.0.0:5002 wsgi:app` para o serviço de `weather_api` e `gunicorn -w 4 --bind 0.0.0.0:5003 wsgi:app ` para o serviço de `newsletter_api`. 
2.1.1. No container de cada serviço execute os comandos para verificar se está tudo certo.

### Configurar o caminho `location` de cada endpoint no arquivo de configurações do nginx `conf.d/nginx.conf`.

3.1 Criar a [imagem](../nginx/Dockerfile) do `nginx` e copiar o [arquivo de configuração](../nginx/conf.d/nginx.conf).
3.2 Atribuir como [volume](../api_flask_compose.yml) o arquivo de configuração no serviço do nginx


## Recomendação de workers | Gunicorn
    
    (2 x num_cores) + 1

## Numero de cores no linux
    
    nproc --all

## Numero de cores no macos
    
    sysctl -n hw.ncpu 


## Links e Referências

- [Nginx | Docs](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [How to Deploy Flask with Gunicorn and Nginx (on Ubuntu) | YouTube](https://youtu.be/KWIIPKbdxD0?si=-THoIOeXyXJV48YY)
- [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
- [Python Flask Tutorial: Deploying Your Application (Option #1) - Deploy to a Linux Server | YouTube](https://youtu.be/goToXTC96Co?si=Mcpd9jlBXp7scZ_S)

